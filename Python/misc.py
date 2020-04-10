import pandas as pd
from sentinelsat import *
from collections import OrderedDict
from datetime import datetime,timedelta, date
import numpy as np
from rasterio.features import sieve
from Python.prep_raster import computeIndexStack,compute_index
from Python.mlc import *
from Python.pred_raster import dtc_pred_stack
from sklearn.cluster import DBSCAN
from glob import glob

def get_feat_layer_order(predictors):
    used_indices = []
    used_bands = []
    
    all_bands_order = ['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B11','B12']
    indices_order = ['NDVI','REP','FAI','GNDVI','NDVI_B8A','VB_FAH','SEI','SABI']
    
    for feature in predictors:
        if feature in indices_order:
            used_indices += [indices_order.index(feature)+1]
        if feature in all_bands_order:
            used_bands += [all_bands_order.index(feature)+1]
            
    return used_indices,used_bands
	

def retrieve_product(date_tiles_dict,api):

    #retrieving product informations
    products = OrderedDict()

    for tile in list(date_tiles_dict.keys()):

        for d in date_tiles_dict[tile]:
            date = datetime.strptime(str(d),'%Y%m%d').date()

            #contrsuct query
            kw_query = {'platformname': 'Sentinel-2',
                        'filename':f'*_{tile}_*',
                        'date':(date, date+timedelta(days=5))} #plus 5 days to get single scene

            #get level-2 products if date> December 2018 
            if date>datetime.strptime(str(20181201),'%Y%m%d').date():
                kw_query['producttype']= 'S2MSI2A'
            else:
                kw_query['producttype']= 'S2MSI1C'

            #retrieve ID used to download the data and store to OrderedDict()      
            pp = api.query(**kw_query)
            products.update(pp)

    #convert to dataframe to view product information (cloud coverage, sensing date, etc.)
    df_products = api.to_dataframe(products)
    return df_products

def semi_sv_pred(nd_array,mlc_model,dtc_model,rescale=True,mlc_thr=7.79,gndvi_thr=0.05,b02_thr=0.15,sieve_size=10):

    """
    Function to predict a numpy ndarray based on trained DTC and MLC models.
    A simple density slicing based on the GNDVI is also employed here.
    
    mlc_thr --> threshold based on the chi square table (n=4)
    gndvi_thr --> threshold for GNDVI image
    b02_thr --> threshold use for creating a cloud mask based on B02
    sieve_size --> minimal sieve size to filter pixel clusters
    """

    if rescale:nd_array = nd_array/10000
    
    b5_b11_img = nd_array[[4,10],:,:]
    b2_img = nd_array[1,:,:]
    
    #DTC, MLC and GNDVI density slicing classifications
    stack2pred_img = np.concatenate((computeIndexStack(nd_array,['NDVI','REP']),b5_b11_img))
    mlc_img = np.where(np.array([mlc_model.classify_raster_gx(stack2pred_img,threshold=mlc_thr)])==3,1,0)
    dtc_img = np.where(np.array([dtc_pred_stack(dtc_model,stack2pred_img)])==3,1,0)
    slice_img = np.array([np.where(compute_index(nd_array,'GNDVI')>=gndvi_thr,1,0)])
    
    #sum classificaiton results 
    arr_sum = np.sum([mlc_img,dtc_img,slice_img],axis=0)
    results = np.where(arr_sum==arr_sum.max(),1,0)
    
    #apply cloud mask and sieve filter (minimum sieve size = 3 pixel)
    cloud_mask = np.where(b2_img>=b02_thr,1,0).astype(int)
    results_masked = np.where(cloud_mask!=1,results,0)
    results_sieved = np.array([sieve(results_masked[0],size=sieve_size)]).astype(np.uint8)
    
    if results_sieved.max()!=0:
        return results_sieved

def dbscan_cluster(gdf_pt_geom,min_dist_km):
    
    #convert points to degree and get lat,lon
    lat = gdf_pt_geom.to_crs(4326).y.values
    lon = gdf_pt_geom.to_crs(4326).x.values
    matrix = np.array([lat, lon]).T
    
    #convert kms to radian unit
    epsilon = min_dist_km / 6371.0088
    
    #perform DBSCAN and get cluster labels
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(matrix))
    cluster_labels = db.labels_+1
    return cluster_labels
	
def get_band_paths(safe_path):
    bands = ['B01_60m','B02_10m','B03_10m','B04_10m','B05_20m','B06_20m',
             'B07_20m','B08_10m','B8A_20m','B09_60m','B11_20m','B12_20m']
    
    return [img for band in bands for img in glob(safe_path + "*/**/*.jp2", recursive=True) if band in img]
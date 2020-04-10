#vector data handling modules
import copy
import os
import re
import json
import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio as rio
from rasterio.mask import mask
from rasterio import Affine
from rasterio.enums import Resampling
from shapely.geometry import shape
from shapely.geometry.multipolygon import MultiPolygon
import rasterio.features
from itertools import product
from rasterio import windows
from tqdm import tqdm,tqdm_notebook

#function to compute index from numpy ndarray 
def compute_index(stack_arr,indextype):
    
    #ignore divide errors when computing indices
    np.seterr(divide='ignore', invalid='ignore')
    
    if indextype == 'NDVI':
        return ((stack_arr[7]-stack_arr[3])/ (stack_arr[7]+stack_arr[3]))
    elif indextype == 'REP':
        return 705+ 35*((((stack_arr[3]+stack_arr[6])/2))-stack_arr[4])/(stack_arr[5]+stack_arr[4])
    elif indextype == "FAI":
        return (stack_arr[7]-(stack_arr[3]+((stack_arr[10]-stack_arr[3])*0.187)))
    elif indextype == "GNDVI":
        return ((stack_arr[7]-stack_arr[2])/ (stack_arr[7]+stack_arr[2]))
    elif indextype == "NDVI_B8A":
        return ((stack_arr[8]-stack_arr[3])/ (stack_arr[8]+stack_arr[3]))
    elif indextype == "VB_FAH":
        return ((stack_arr[7]-stack_arr[2])+((stack_arr[2]-stack_arr[3])*0.614))
    elif indextype == "SEI":
        return ((stack_arr[7]-stack_arr[10])/ (stack_arr[7]+stack_arr[10]))
    elif indextype == "SABI":
        return ((stack_arr[7]-stack_arr[3])/ (stack_arr[1]+stack_arr[2]))
    else:
        print('Specify an indextype')

def computeIndexStack(clipped_file,indices,out_file=None):

    if type(clipped_file)==str:
        with rio.open(clipped_file) as src:
            img = src.read()
            meta = src.meta.copy()
            meta.update(count=len(indices),nodata=999,dtype=rio.float32)

        with rio.open(out_file,'w',**meta) as dst:
            index_img = np.array([compute_index(img,index).astype(rio.float32) for index in indices])
            dst.write(index_img)
            
    elif type(clipped_file)==np.ndarray:
        return np.array([compute_index(clipped_file,index).astype(rio.float32) for index in indices])


def stack_bands(band_paths,reference_10m,out_file):
     
    with rio.open(reference_10m) as src0:
        meta = src0.meta
        meta.update(count = len(band_paths),driver='GTiff')
        
        height = int(src0.height)
        width = int(src0.width)

        with rio.open(out_file,'w',**meta) as dst:
            
            for i,layer in enumerate(tqdm(band_paths,position=0, leave=True),start=1):
                if '_10m' in layer:
                    with rio.open(layer) as src10m:
                        dst.write_band(i,src10m.read(1))    
                elif '_20m' in layer:
                    with rio.open(layer) as src20m:
                        data = src20m.read(1,out_shape = (height,width),resampling = Resampling.bilinear)
                        dst.write_band(i,data)
                elif '_60m' in layer:
                    with rio.open(layer) as src60m:
                        data = src60m.read(1,out_shape = (height,width),resampling = Resampling.bilinear)
                        dst.write_band(i,data)

def clip_raster(image_path, clip_file,out_file=None,fill=False,invert=False,crop=True,nodat=None,export=True):
    
    if type(clip_file)==str:
        geometry = [json.loads(gpd.read_file(clip_file).to_json())['features'][0]['geometry']]
    else:
        geometry = clip_file
    
    with rio.open(image_path) as src:
        out_meta = src.meta.copy()
        if nodat==None:
            nodat=src.nodata
        
        out_img, out_transform = mask(dataset=src,shapes=geometry,crop=crop,nodata=nodat,all_touched=True,filled=fill,pad=False,invert=invert)
        out_img = out_img.astype(rio.float32)/10000
        if export:
            out_meta.update({"driver":"GTiff","height": out_img.shape[1],"width": out_img.shape[2],"transform": out_transform,'nodata':nodat,"dtype":rio.float32})

            with rio.open(out_file,'w',**out_meta) as dst:
                dst.write(out_img)
        else:
            return out_img,out_transform
            
#function to extract values from stack base don geojson feature
def pixel_sample(stack_path,geojson_path,bands_list):

    #load feature
    train_sites = gpd.read_file(geojson_path)
    features = json.loads(train_sites.to_json())['features']
    date = re.findall(r"_(\d{8})_", geojson_path)[0]

    #stack to be filled with dummy dfs
    df_stack = []

    #load image
    with rio.open(stack_path) as src:
        for feature in features:

            #create dummy dictionary for every feature
			#these property names originate from QGIS Semi-Automatic Classiﬁcation Plugin
            data = {
                'C' : feature['properties']['C_info'],
                'MC' : feature['properties']['MC_info'],
                'SCP_UID' : feature['properties']['SCP_UID'],
                'date':date}
            
            #clip image based on feature and iterate over each image to extract its values
            out_img= mask(dataset=src,shapes=[feature['geometry']],crop=True)[0]
            for band_nr,array in enumerate(out_img):
                values = np.extract(array!=src.nodata,array)
                data[bands_list[band_nr]]=values
                
            #convert dictionary to dataframe and insert to stack
            df_stack.append(pd.DataFrame(data))
            
    #concatenate dfs
    specsign_df = pd.concat(df_stack,ignore_index=True)

    return specsign_df         
     
def polygonize(image,pixel_value,src_transform,src_crs,out_file,centroid=True):
    #get pixel shapes
    shapes = list(rasterio.features.shapes(image, transform=src_transform))
    shapes = list(filter(lambda x: x[1]==pixel_value, shapes))

    #convert into geodataframe
    multipolygon = MultiPolygon([shape(geom[0]) for geom in shapes])
    data=[]
    for poly in multipolygon:
        gdf = gpd.GeoDataFrame(geometry=[poly],crs=src_crs) 
        data.append(gdf)
    data = pd.concat(data,ignore_index=True)
    data['area_m2'] = data.area.astype(int)
    if centroid:
        data['geometry'] =data['geometry'].centroid
    if out_file is not None:
        data.to_file(out_file,driver='GeoJSON')
    else:
        return data
 
def get_tiles(src,nr_tiles):
    
    if nr_tiles <36:

        scale = int(np.ceil(np.sqrt(nr_tiles)))
        size = int(src.meta['width']/scale)

        #get original image dimension
        ncols, nrows = src.meta['width'], src.meta['height']

        #define offsets (iterator) based on specified tile size
        offsets = product(range(0, ncols, size), range(0, nrows, size))

        #create a large tile from original image dimension 
        big_window = windows.Window(col_off=0,row_off=0,width=ncols,height=nrows)

        #find intersection with the large tile and get the tile dimension and affine
        tiles = []
        for col_off,row_off in offsets:
            tile = windows.Window(col_off=col_off, row_off=row_off, width=size, height=size).intersection(big_window)
            tile_affine = windows.transform(tile, src.transform)
            tiles.append((tile,tile_affine))
        return tiles
    else:
        print('Try number of tiles < 36')
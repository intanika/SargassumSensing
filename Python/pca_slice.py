import pandas as pd
from sklearn.decomposition import PCA
from rasterio.plot import reshape_as_raster, reshape_as_image
import rasterio as rio
import numpy as np
from skimage.filters import threshold_triangle

def compute_pca_image(file,band_order,nr_components,outfile=None):
    
    #read all bands (except B9 and B1 = 60m) and metadata
    
    with rio.open(file) as src:
        img = src.read(band_order)
        profile = src.profile.copy()
        
        arr = reshape_as_image(img).reshape(-1,len(img))
        PC = PCA(n_components=nr_components,random_state = 42).fit(arr)

        #perform orthogonal projection/ transformation (rotation) of the array into the vector space of fitted PC 
        #also reduces the dimensionality (bands) into 1D space
        PC_transformed = PC.transform(arr)
        
        #reshape to 2d
        PC_2d=PC_transformed.reshape(img.shape[1],img.shape[2],nr_components)
        
        # rescale to 0-65535 values 16bit datatype to reduce further k-means clustering time
        PC_2d_Norm = np.zeros((img.shape[1],img.shape[2],len(img)))
        for i in range(nr_components):
            PC_2d_Norm[:,:,i] = ((PC_2d[:,:,i] - PC_2d[:,:,i].min()) * (1/(PC_2d[:,:,i].max() - PC_2d[:,:,i].min()) * 65535))
        
        #reshape to raster
        pca_img = reshape_as_raster(PC_2d)[0:,:,:]
        
        #output
        profile.update({'nodata': None,'dtype': rio.float32,'count':len(pca_img),'width':img.shape[2],'height':img.shape[1]})
        
        if outfile is not None:
            with rio.open(outfile, 'w', **profile) as dst:
                dst.write(pca_img.astype(rio.float32))
        else:
            return pca_img.astype(rio.float32)
 
def compute_pca_score(file,band_order,bands,nr_components,subset_name=None):
    
    expvar_data = {}
    
    #read all bands (except B9 and B1 = 60m) and metadata
    with rio.open(file) as src:
        img = src.read(band_order)
        profile = src.profile.copy()

        arr = reshape_as_image(img).reshape(-1,len(img))
        PC = PCA(n_components=nr_components,random_state = 42).fit(arr)
        
        eigenvectors_df = pd.DataFrame(PC.components_,columns=bands,index = [f'PC{str(i)}' for i in range(1,nr_components+1)])
        eigenvectors_df = round(eigenvectors_df,3)
        expvar_data['variance'] = PC.explained_variance_ratio_
        if subset_name!= None:
            eigenvectors_df['subset'] = subset_name
        
        
    pc_nr = [f'PC{str(i)}' for i in range(1,nr_components+1)]
    expvar_df = pd.DataFrame(expvar_data,index=pc_nr).round(4)
    score = pd.concat([eigenvectors_df,expvar_df],axis=1)
    return(score) 

def pca_triangle(file,pc_band,outfile=None):
    
    if type(file)==str:
        with rio.open(file) as src:
            profile = src.profile.copy()

            #triangle thresholding
            thr = threshold_triangle(src.read([pc_band]))
            img_bin = np.where(src.read([pc_band])>thr,1,0)

            #output
            profile.update({'nodata': 0,'dtype': rio.uint8,'count':1})

            if outfile != None:
                with rio.open(outfile, 'w', **profile) as dst:
                    dst.write(img_bin.astype(rio.uint8))
            else:
                return img_bin.astype(rio.uint8)
    elif type(file)== np.ndarray:
        thr = threshold_triangle(file[pc_band])
        img_bin = np.where(file[pc_band]>thr,1,0)
        return img_bin.astype(rio.uint8)
			
def density_slice(file,band,thr,outfile=None):
    
    with rio.open(file) as src:
        profile = src.profile.copy()
        img_bin = np.where(src.read([band])>=thr,1,0)
        profile.update({'nodata': 0,'dtype': rio.uint8,'count':1})
        
        if file != None:
            with rio.open(outfile, 'w', **profile) as dst:
                dst.write(img_bin.astype(rio.uint8))
        else:
            return img_bin.astype(rio.uint8)		

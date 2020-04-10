from rasterio.plot import reshape_as_raster, reshape_as_image
from sklearn.tree import DecisionTreeClassifier
import rasterio as rio
import numpy as np
from sklearn.decomposition import PCA

def stack2pred(stack_index=None,stack_band=None,index_sel=None,band_sel=None,outfile=None):
    
    """
    Function to stack index and band images together. 
    """

    if (stack_index is not None and index_sel is not None and stack_band is not None and band_sel is not None):
    
        count_new_stack = len(index_sel+band_sel)

        with rio.open(stack_index) as src1:
            img_indices = src1.read(index_sel)

            img_indices[np.isnan(img_indices)]=999

        with rio.open(stack_band) as src2:
            img_bands = src2.read(band_sel)
            meta =  src2.meta
            meta.update(count=count_new_stack,dtype='float32',nodata=999)

            out_img = np.vstack((img_indices,img_bands))

        with rio.open(outfile,'w',**meta) as dst:
            for i in range(len(out_img)):
                dst.write_band(i+1,out_img[i])
                
    elif (stack_index == None and index_sel == None):
        
        count_new_stack = len(band_sel)
        with rio.open(stack_band) as src2:
            img_bands = src2.read(band_sel)
            meta =  src2.meta
            meta.update(count=count_new_stack)
            
        with rio.open(outfile,'w',**meta) as dst:
            for i in range(len(img_bands)):
                dst.write_band(i+1,img_bands[i])
                
    elif (stack_band == None and band_sel == None):
        count_new_stack = len(index_sel)

        with rio.open(stack_index) as src1:
            img_indices = src1.read(index_sel)

            meta =  src1.meta
            meta.update(count=count_new_stack)
            
        with rio.open(outfile,'w',**meta) as dst:
            for i in range(len(img_indices)):
                dst.write_band(i+1,img_indices[i])


def dtc_pred_stack(model,stack2pred_img,outfile=None):

    """
    Function to classfy raster stack image 
    """
    if type(stack2pred_img)==str:
        with rio.open(stack2pred_img) as src:
            img = src.read()
            profile = src.profile
            reshaped_img = reshape_as_image(img)
            raster_pred = model.predict(reshaped_img.reshape(-1,len(img)))
            class_prediction = raster_pred.reshape(reshaped_img[:, :, 0].shape)
            class_prediction = class_prediction + 1
            profile.update({'nodata': 0,'dtype': rio.uint8,'count':1})

        with rio.open(outfile, 'w', **profile) as dst:
            dst.write(class_prediction.astype(rio.uint8), 1)
            
    elif type(stack2pred_img)==np.ndarray:
        stack2pred_img[np.isnan(stack2pred_img)]=0
        reshaped_img = reshape_as_image(stack2pred_img)
        raster_pred = model.predict(reshaped_img.reshape(-1,len(stack2pred_img)))
        class_prediction = raster_pred.reshape(reshaped_img[:, :, 0].shape)
        class_prediction = class_prediction + 1
        return class_prediction.astype(rio.uint8)
 

        

        
        
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import rasterio as rio
from rasterio.plot import reshape_as_raster, reshape_as_image


# In[408]:


class mlClassifier:
    """
    A simple ML classifier class. No a priori probability (equal probability for each class).
    Adapted from:https://gist.github.com/jgomezdans/8276704#file-ml_test-ipynb
    Credits to J Gomez-Dans 
    """
    
    def __init__(self,train,label_column):
        """
        Takes in a training dataset as panda dataframe, n_features*n_samples
        (i.e. columns * rows), column name of the labels and image stack to predict (optional).
        Pre computes log determinant of the training dataset.
        """
        
        self.train_labels = train[label_column].unique()
        self.label_column = label_column
        self.train = train
        self.mus,self.i_covs,self.det_covs = self.compute_density()

    def compute_density(self):
        
        mus = []
        i_covs= []
        det_covs = []
        for label in self.train_labels:
            train_subset = self.train[self.train[self.label_column]==label]
            train_subset = train_subset.drop(columns=[self.label_column])
            train_subset = np.transpose(train_subset.to_numpy())
            n_samples = train_subset.shape[1]
            n_features = train_subset.shape[0]
            cov_m = np.cov(train_subset)
            i_cov_m = np.linalg.inv(cov_m)
            det_cov = np.linalg.det(cov_m)
            mu = train_subset.mean(axis=1)
            
            mus.append(mu)
            i_covs.append(i_cov_m)
            det_covs.append(det_cov)
            
        return (mus,i_covs,det_covs)
    
    def calc_prob(self,x_test,mu,i_cov_m):
        """
        Method to compute the (class) conditional probability density
        """
        s = x_test - mu
        log_prob = -0.5*(np.dot(s,i_cov_m)*s).sum(1)
        prob = np.exp(log_prob)
        return prob
    
    def calc_prob_gx(self,x_test,mu,i_cov_m,det_cov,threshold):
        
        """
        Method to compute the gaussian discrimnant function with threshold 
        """
        
        s = x_test - mu
        gx = -np.log(det_cov)-(np.dot(s,i_cov_m)*s).sum(1)
        if threshold :
            t = -threshold - np.log(det_cov)
            gx = np.where(gx>t,gx,99)
            return gx
        else:
            return gx
        
    def img2predict(self,stack_img):
        """
        Method to load an image as rasterio object
        """
        with rio.open(stack_img) as src:
            img = src.read()
            profile = src.profile
            return (img,profile)
                 
    def prob_rasters(self,stack_img,out_file):
        """
        Method to compute the calculate the probability of a raster image.
        """
        
        img,profile = self.img2predict(stack_img)
        
        profile.update({'driver': 'GTiff','interleave': 'band','compress': 'lzw',
                        'width':img.shape[2],'height':img.shape[1],
                        'nodata': -999,'dtype': rio.float32,'count':len(self.train_labels)
                       })
        
        reshaped_img = reshape_as_image(img)
        raster_pred = reshaped_img.reshape(-1,len(img))

        stack=[]
        for i in range(len(self.train_labels)):
            mu = self.mus[i]
            i_cov_m = self.i_covs[i]
            prob_img = self.calc_prob(raster_pred,mu,i_cov_m)

            prob_reshaped_img = prob_img.reshape(reshaped_img[:,:,0].shape)

            stack.append([prob_reshaped_img])
        out_img = np.vstack(stack)

        with rio.open(out_file,'w',**profile) as dst:
            for i in range(len(out_img)):
                dst.write_band(i+1,out_img[i].astype(rio.float32))
                
    def classify_raster_gx(self,stack_img,out_file=None,threshold=None):
        """
        Method to compute the discrimnant function, find the max likelihood and assign classes to a raster image.
        Threshold is based on the N-degrees of freedom (N = number of predictors) and Chi-Square
        """
        if type(stack_img)==str:
            img,profile = self.img2predict(stack_img)

            reshaped_img = reshape_as_image(img)
            raster_pred = reshaped_img.reshape(-1,len(img))

            profile.update({'driver': 'GTiff','interleave': 'band','compress': 'lzw',
                            'width':img.shape[2],'height':img.shape[1],
                            'nodata': 99,'dtype': rio.uint8,'count':1})
							
        elif type(stack_img)==np.ndarray:
            reshaped_img = reshape_as_image(stack_img)
            raster_pred = reshaped_img.reshape(-1,len(stack_img))
        
        if threshold is None:
            stack=[]
            for i in range(len(self.train_labels)):
                mu = self.mus[i]
                i_cov_m = self.i_covs[i]
                det_cov = self.det_covs[i]

                prob_img = self.calc_prob_gx(raster_pred,mu,i_cov_m,det_cov,threshold)
                stack.append([prob_img])

            vstack = np.vstack(stack)

            class_stack = np.argmax(vstack,axis=0)+1
            class_image = class_stack.reshape(reshaped_img[:,:,0].shape)

        else:

            stack=[]
            for i in range(len(self.train_labels)):
                mu = self.mus[i]
                i_cov_m = self.i_covs[i]
                det_cov = self.det_covs[i]

                prob_img = self.calc_prob_gx(raster_pred,mu,i_cov_m,det_cov,threshold)
                stack.append([prob_img])
            vstack = np.vstack(stack)
            
            mask= np.where(vstack==99,vstack,0)
            mask = np.sum(mask,axis=0)
            mask = np.where(mask==mask.max(),mask,0)
            
            new_vstack = np.where(vstack!=99,vstack,0)
            new_vstack = np.vstack((new_vstack,mask))
            
            class_stack = np.argmax(new_vstack,axis=0)+1
            class_image = class_stack.reshape(reshaped_img[:,:,0].shape)
        
        if out_file is None:
            return class_image
        else:
            with rio.open(out_file,'w',**profile) as dst:
                dst.write(class_image.astype(rio.uint8),1)
    
    def classify_testdata(self,x_test,label_column,threshold=None):
        """
        Method for accuracy assessment.
        Return oa,kappa,acc_df,con_mat
        """
        
        test_df = x_test.copy()
        all_columns = test_df.columns
        predictors = [i for i in x_test.columns if i != label_column]
        x_test = x_test[predictors]
        x_test = x_test.to_numpy()
        
        for i,label in enumerate(self.train_labels):
            mu = self.mus[i]
            i_cov_m = self.i_covs[i]
            det_cov = self.det_covs[i]
            
            prob_data = self.calc_prob_gx(x_test,mu,i_cov_m,det_cov,threshold)
            test_df[label+"_gx"] = prob_data
        
        
        labels_gx = np.setdiff1d(test_df.columns,all_columns)

        if threshold is None:
            test_df['MLC predicted'] = test_df[labels_gx].idxmax(axis=1).str.split('_').str[0]
        else:
            test_df['MLC predicted'] = test_df[labels_gx].where(test_df[labels_gx]!=99).idxmax(axis=1).str.split('_').str[0]
            
        
        test_df = test_df.dropna()[[label_column,'MLC predicted']]
        
        
        #create confusion matrix
        con_mat = pd.crosstab(test_df[label_column],test_df['MLC predicted'])
        con_mat.columns.name = 'MLC'
        
        #compute user, producer and overall accuracies
        row_sum = con_mat.sum(axis=1)
        col_sum = con_mat.sum(axis=0)
        omitted = np.setdiff1d(col_sum.index,row_sum.index)
        col_sum = col_sum.drop(omitted)
        
        ua = np.diag(con_mat)/row_sum
        pa = np.diag(con_mat)/col_sum
        f1 = (2 * pa*ua) /(pa+ua)
        oa = sum(np.diag(con_mat))/len(test_df)
        acc_df =  round(pd.DataFrame({'Label':col_sum.index,'PA':pa.values,'UA':ua.values,'F1-score':f1.values}),2)
        
        #compute kappa score (khat)
        p = row_sum/ len(test_df)
        q = col_sum/len(test_df)
        exp_acc = sum(p*q)
        kappa = (oa-exp_acc)/(1-exp_acc)

        con_mat = con_mat.append(pd.Series(con_mat.sum(0),name='Observed'))
        con_mat['Classified'] = pd.Series(con_mat.sum(1))
        con_mat = con_mat.append(acc_df.set_index('Label')["PA"])
        con_mat["UA"] = acc_df.set_index('Label')["UA"] 
        con_mat["F1-score"] = acc_df.set_index('Label')["F1-score"]
        con_mat.iloc[-1,-2] = f'{round(oa,2)} (OA)'
        con_mat.iloc[-1,-1] = f'{round(kappa,2)} (Kappa)'
        con_mat = con_mat.fillna('-')
        accuracy_table = con_mat[con_mat!=0.0].fillna('-')

        return accuracy_table

        



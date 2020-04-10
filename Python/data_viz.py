import matplotlib.pyplot as plt
from matplotlib.legend import Legend
import seaborn as sns
import numpy as np
import json
import geopandas as gpd
import rasterio as rio
from rasterio.mask import mask
import numpy as np
from rasterio.plot import adjust_band
from rasterio.plot import reshape_as_raster, reshape_as_image
from rasterio.plot import show
from skimage.color import rgb2gray
from skimage import exposure
from matplotlib import colors
import matplotlib.patches as mpatches
from matplotlib import cm
import joypy
import pandas as pd
import warnings

def validation_curve_plot(train_scores,test_scores,parameter,xlabel_text,axs):
    # Calculate mean and standard deviation for training set scores
    train_mean = np.mean(train_scores, axis=1)
    
    # Calculate mean and standard deviation for test set scores
    test_mean = np.mean(test_scores, axis=1)

    # Plot mean accuracy scores for training and test sets
    axs.plot(parameter, train_mean, label="Training accuracy", color="green")
    axs.plot(parameter, test_mean, label="Cross-validation (K=10) accuracy", color="blue")

    # Create plot
    axs.set_xlabel(xlabel_text)
    axs.set_ylabel("Accuracy")
    plt.tight_layout()
    axs.legend(loc="best")


def specsign_plot(dataframe,bands,classtype,focus_class=None):
    
    plt.style.use('bmh')
    classes = list(dataframe[classtype].unique())

    if classtype=='MC':col_list = ['red', 'blue', 'chocolate','green']
    elif classtype=='C':col_list = ['black','black','deepskyblue','royalblue','gold','chocolate','green','yellowgreen']
        
    fig,ax = plt.subplots(1,1,figsize=[10,8])
    
    if classtype == "MC":plt.title(f'Spectral signature macroclasses',fontsize=16)
    else:plt.title(f'Spectral signature subclasses',fontsize=16)
    
    for i,c in enumerate(classes):
        df_melt = dataframe[dataframe[classtype]==c][bands].melt()

        #plot mean value for each band
        mean = df_melt.groupby('variable')['value'].mean().reindex(bands)
        
        if c=='Sf':lineplot = ax.plot(bands,mean,label=c,color=col_list[i],ls='--')
        else:lineplot = ax.plot(bands,mean,label=c,color=col_list[i])

        #plot mean reflectance with CI of 95%
        ax.set_xticklabels(bands, rotation = 45, ha="right",fontsize=16)
        ax.set_ylabel('Surface Reflectance',fontsize=16)
        ax.legend(loc='upper left',fontsize=12)
        ax.tick_params(axis="both", labelsize=12)
      
    plt.show()

 #plot JMD values into a heatmap

def jmd_heatmap(jmd_df_list):
    fig,axs = plt.subplots(3,4,figsize=(20,13),sharex=True,sharey=True)
    axs = axs.ravel() 

    cbar_ax = fig.add_axes([0.3, 1, .4, .02])

    for i,jmd_df in enumerate(jmd_df_list):

        #copy df to avoid mutating original input df
        jmd_df_copy = jmd_df.copy()

        #get band name and remove the band resolution suffix from column names
        band_name = jmd_df_copy.columns[0].split('_')[0]
        
        jmd_df_copy.columns = list(jmd_df_copy.columns.str.split('_').str[-1])[::-1]
        jmd_df_copy.index = list(jmd_df_copy.index.str.split('_').str[-1])[::-1]

        #create mask for JMD duplicates in upper rows and columns
        mask = np.zeros_like(jmd_df_copy)
        mask[np.triu_indices_from(mask)] = True

        jmd_heatmap = sns.heatmap(jmd_df_copy,annot=True,annot_kws={"size": 15},fmt=".1f",cmap='RdYlGn',
                                  mask=mask,alpha = 0.7,linewidths=0.5,ax=axs[i],
                                  cbar=i == 0,cbar_ax=None if i else cbar_ax,
                                  cbar_kws={'alpha':0.5,'orientation':'horizontal'},
                                 vmin=1,vmax=2)
        axs[i].text(5.5,1,band_name,fontsize=20)
        axs[i].tick_params(axis="both", labelsize=15)
        
        #fix bottom half cut off
        bottom, top = jmd_heatmap.get_ylim()
        jmd_heatmap.set_ylim(bottom + 0.5, top - 0.5)
    
    cbar_ax.tick_params(labelsize=15)
    cbar_ax.xaxis.set_ticks_position('top')
    plt.title('Jeffries-Matusita distance',fontsize=25)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.tight_layout()
        
    plt.show()      
    
def ridgePlot(subset_df,target_col):
    for i,col in enumerate(subset_df.columns[subset_df.columns!=target_col]):
        xmin,xmax = subset_df[col].min(),subset_df[col].max()
        steps = (xmax-xmin)/8
        joyplot = joypy.joyplot(data= subset_df,by=target_col,column=col,labels=list(subset_df.groupby(target_col).count().index),
                                x_range=[xmin-steps,xmax+steps],overlap=1,figsize=(7,5),
                                linecolor="gray",title=f"{col} Distribution",hist="True", bins=60,lw=1,histtype='stepfilled',color='#8ac6d1',density=True)

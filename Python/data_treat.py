
import pandas as pd
import numpy as np


#balancing number of samples for earch class/ macroclass in the dataframe
#downsampling is performed in this function which involves randomly removing observations from the majority class 
def down_sample (dataframe,classtype,c):

    labels = list(dataframe[classtype].unique())
    
    sample_size = len(dataframe[dataframe[classtype]==c])

    to_downsample = []
    to_retain = []
    for label in labels:
        sample_size_label = len(dataframe[dataframe[classtype]==label])
        if (c != label) and (sample_size_label >sample_size) and (sample_size_label != sample_size):
            to_downsample.append(label)
        else:
            to_retain.append(label)
    
    df_retained = dataframe[dataframe['C'].isin(to_retain)]
    
    
    df_label_downsampled = []
    for down_label in to_downsample:
        label_downsampled = dataframe[dataframe[classtype]==down_label].sample(n=sample_size,random_state=42)
        df_label_downsampled.append(label_downsampled)
    df_label_downsampled = pd.concat(df_label_downsampled,axis=0)
    
    df_downsampled = pd.concat([df_retained,df_label_downsampled],axis=0).reset_index(drop=True)
    return df_downsampled
    

def balance_sample (df,class_type,majority_class=None):

    sample_sizes = df.groupby(class_type).count().values[:,0]
    labels = list(df.groupby(class_type).count().index)
    
    df_balanced = []
    
    if majority_class in labels:
        new_sample_size = sample_sizes[labels.index(majority_class)]
        
    for i in range(len(sample_sizes)):
        if sample_sizes[i]>new_sample_size: 
            class_df = df[df[class_type]==labels[i]].sample(n=new_sample_size,random_state=42).reset_index(drop=True)
            df_balanced.append(class_df)
        elif sample_sizes[i]<new_sample_size:

            #compute band mean of the smaller classes
            class_mean = df[df[class_type]==labels[i]].groupby(class_type).mean().reset_index()
            add_col = pd.DataFrame(df[df[class_type]==labels[i]][np.setdiff1d(df.columns,class_mean.columns)].iloc[0,:]).T.reset_index(drop=True)
            add_col['SCP_UID'] = 'upsampled_mean'
            class_mean = pd.concat([class_mean, add_col], axis=1)[df.columns]

            #append the band mean * new_sample_size to the class dataframe subset
            class_df = df[df[class_type]==labels[i]]
            class_df = class_df.append([class_mean]*(new_sample_size-sample_sizes[i])).reset_index(drop=True)
            df_balanced.append(class_df)

        elif sample_sizes[i]==new_sample_size:
            class_df = df[df[class_type]==labels[i]].reset_index(drop=True)
            df_balanced.append(class_df)
    
    return pd.concat(df_balanced)
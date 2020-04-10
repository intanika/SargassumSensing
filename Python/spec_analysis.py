import pandas as pd
import numpy as np

#function to compute separability between the classes in each vegetation index (feature)
def jmd_calc(index_class_1,index_class_2):
    
    #compute Bhattacharyya distance of two classes
    c1 = np.nanvar(index_class_1)
    c2 = np.nanvar(index_class_2)
    m1_m2 = (np.nanmean(index_class_1)-np.nanmean(index_class_2))**2
    term_1 = 0.125*m1_m2*(2/(c1+c2))
    term_2 = 0.5*np.log((c1+c2)/ (2*np.sqrt(c1)*np.sqrt(c2) ))
    BD = term_1 + term_2

    #compute Jeffries Matusita distance [0-2]
    JMD = 2*(1-np.exp(-BD))
    return JMD

def transpose_df(df,classtype,index):
    classes = df[classtype].unique()
    index_class = df[[classtype,index]]
    
    df = {}
    for i,c in enumerate(classes):
        data = np.array(index_class[index_class[classtype]==c][index])
        df[f"{index}_{c}"] = data
    df = pd.DataFrame.from_dict(df, orient='index').T
    return df 


def jmd2df(df_index_transposed):

    df=pd.DataFrame()

    for i,name in enumerate(df_index_transposed.columns):
        c1_name = df_index_transposed.iloc[:,i].name
        c1 = df_index_transposed.iloc[:,i]

        vector = []

        for i,name in enumerate(df_index_transposed.columns):
            c2_name = df_index_transposed.iloc[:,i].name
            c2 = df_index_transposed.iloc[:,i]
            JMD = jmd_calc(c1,c2)
            vector.append(JMD)

        df.insert(0,f"{c1_name}",vector)

    df = df[::-1]
    df.set_index(df.columns,inplace=True)
    df = df.round(3)
    
    return df
    
    
    
    
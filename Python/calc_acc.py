import pandas as pd
import numpy as np

def calc_acc(y_test,y_pred):

    con_mat = pd.crosstab(pd.Series(y_test,name='Observed'),pd.Series(y_pred,name='DTC'))
                          
    missing = np.setdiff1d(con_mat.columns,con_mat.index)
    
    if len(missing)>0:
        new_mat = con_mat.reset_index()
        for c in missing:
            new_mat = new_mat.append(pd.Series(0, index=con_mat.columns), ignore_index=True)
            new_mat.at[(len(new_mat['DTC'])-1),'DTC'] = c
        new_mat.set_index('DTC',inplace=True)
        con_mat = new_mat.reindex(index=con_mat.columns)
        

    row_sum = con_mat.sum(axis=1)
    col_sum = con_mat.sum(axis=0)
    omitted = np.setdiff1d(col_sum.index,row_sum.index)
    col_sum = col_sum.drop(omitted)
    
    ua = np.diag(con_mat)/row_sum
    pa = np.diag(con_mat)/col_sum
    f1 = (2 * pa*ua) /(pa+ua)
    
    oa = sum(np.diag(con_mat))/len(y_test)
    acc_df = round(pd.DataFrame({'Label':col_sum.index,'PA':pa.values,'UA':ua.values,'F1-score':f1.values}),2).fillna(0)

    #kappa score 
    p = row_sum/ len(y_test)
    q = col_sum/len(y_test)
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

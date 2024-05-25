import pickle
import pandas as pd
import numpy as np


with open('sources/data/model_xgb_MEE.pkl', 'rb') as f:
    model_MEE = pickle.load(f)
    
with open('sources/data/model_xgb_EKMP.pkl', 'rb') as f:
    model_EKMP = pickle.load(f)
    
with open('sources/data/sort_list_MEE.pkl', 'rb') as f:
    sort_list_MEE = pickle.load(f)
    
with open('sources/data/sort_list_EKMP.pkl', 'rb') as f:
    sort_list_EKMP = pickle.load(f)
    
    
def predict_MEE(df, df_PD): 
    df=df[sort_list_MEE]   
    pred = pd.DataFrame(model_MEE.predict_proba(df), columns=['В отбор МЕЕ','Дефект МЕЕ','Не подлежит МЕЕ'])    
    ret_df = pd.concat([df_PD, pred], axis=1)
    return ret_df

    
def predict_EKMP(df, df_PD):    
    df=df[sort_list_EKMP]
    pred = pd.DataFrame(model_EKMP.predict_proba(df), columns=['В отбор ЭKMP','Дефект ЭKMP','Не подлежит ЭKMP'])    
    ret_df = pd.concat([df_PD, pred], axis=1)
    return ret_df

def predict_all(df_MEE, df_EKMP, df_PD):     
    df_MEE=df_MEE[sort_list_MEE]
    df_EKMP=df_EKMP[sort_list_EKMP]
    pred_MEE = pd.DataFrame(model_MEE.predict_proba(df_MEE), columns=['В отбор МЕЕ','Дефект МЕЕ','Не подлежит МЕЕ'])  
    pred_EKMP = pd.DataFrame(model_EKMP.predict_proba(df_EKMP), columns=['В отбор ЭKMP','Дефект ЭKMP','Не подлежит ЭKMP']) 
    ret_df = pd.concat([df_PD, pred_MEE], axis=1)
    ret_df = pd.concat([ret_df, pred_EKMP], axis=1)
    return ret_df
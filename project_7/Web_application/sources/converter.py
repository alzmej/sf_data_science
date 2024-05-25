# Импорт необходимых библиотек
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, QuantileTransformer, TargetEncoder
from sklearn.model_selection import train_test_split 
from sklearn.pipeline import Pipeline
import pickle
from sources.functions import group_omu_convert, ds0_ds1, diff_dates, type_converter

# загрузим служебную информацию
with open('sources/data/col_list.pkl', 'rb') as f:
    col_list = pickle.load(f)
    
with open('sources/data/num_cols_MEE.pkl', 'rb') as f:
    num_cols_MEE = pickle.load(f)
        
with open('sources/data/num_cols_EKMP.pkl', 'rb') as f:
    num_cols_EKMP = pickle.load(f)
    
with open('sources/data/skte_MEE.pkl', 'rb') as f:
    skte_MEE = pickle.load(f)
    
with open('sources/data/skte_EKMP.pkl', 'rb') as f:
    skte_EKMP = pickle.load(f)
    
with open('sources/data/columns_dict_trans_MEE.pkl', 'rb') as f:
    columns_dict_trans_MEE = pickle.load(f)
    
with open('sources/data/columns_dict_trans_EKMP.pkl', 'rb') as f:
    columns_dict_trans_EKMP = pickle.load(f)
    
with open('sources/data/base_col_list_MEE.pkl', 'rb') as f:
    base_col_list_MEE = pickle.load(f)
    
with open('sources/data/base_col_list_EKMP.pkl', 'rb') as f:
    base_col_list_EKMP = pickle.load(f)

data_MO = pd.read_csv('sources/data/MO.csv', names=['MO', 'OKFS', 'MO_level', 'attach', 'population'])

# инициируем переменные
RANDOM_STATE=42
drop_list = []


def add_columns_MEE(data):
    """ Функция для дополнеия датасета колонками,
    отсутствующими в связи с отличием входных данных
    от тренировочных
    
    Args:
        - data: входной датасет
    Returns:
        - датасет с недостающими колонками
    """
    df_col_list = data.columns
    for item in df_col_list:
        if item == 'SMO_83001':
            data['SMO_83001.0'] = data['SMO_83001']
            data = data.drop(['SMO_83001'], axis = 1)
        elif item == 'SMO_83005':
            data['SMO_83005.0'] = data['SMO_83005']
            data = data.drop(['SMO_83005'], axis = 1)
        elif item == 'SMO_83008':
            data['SMO_83008.0'] = data['SMO_83008']
            data = data.drop(['SMO_83008'], axis = 1)
    df_col_set = set(data.columns)
    base_col_set = set(base_col_list_MEE)
    add_col_list = list(base_col_set-df_col_set)
    add_df = pd.DataFrame(np.zeros((data.shape[0],len(add_col_list)), dtype=np.float32), columns=add_col_list)
    data = pd.concat([data, add_df], axis=1)
    
    return data


def add_columns_EKMP(data):
    """ Функция для дополнеия датасета колонками,
    отсутствующими в связи с отличием входных данных
    от тренировочных
    
    Args:
        - data: входной датасет
    Returns:
        - датасет с недостающими колонками
    """
    df_col_list = data.columns
    for item in df_col_list:
        if item == 'SMO_83001':
            data['SMO_83001.0'] = data['SMO_83001']
            data = data.drop(['SMO_83001'], axis = 1)
        elif item == 'SMO_83005':
            data['SMO_83005.0'] = data['SMO_83005']
            data = data.drop(['SMO_83005'], axis = 1)
        elif item == 'SMO_83008':
            data['SMO_83008.0'] = data['SMO_83008']
            data = data.drop(['SMO_83008'], axis = 1)
    df_col_set = set(data.columns)
    base_col_set = set(base_col_list_EKMP)
    add_col_list = list(base_col_set-df_col_set)
    add_df = pd.DataFrame(np.zeros((data.shape[0],len(add_col_list)), dtype=np.float32), columns=add_col_list)
    data = pd.concat([data, add_df], axis=1)
    
    return data


def convert_df(data):
    """ Функция для преобразования данных перед их 
    приведением в состояние пригодное для подачи
    в модель для проведения предсказания
    
    Args:
        - data: входной датасет
    Returns:
        - конвертированный датасет
    """
    # объединим датасеты
    data = data.merge(data_MO, how = 'left', on ='MO')

    #удалим дубликаты
    data=data.drop_duplicates()

    # преобразуем признаки
    data['GROUP_OMU'] = data['GROUP_OMU'].map(group_omu_convert)
    data['NPR_DATE'] = pd.to_datetime(data['NPR_DATE'], format='%d.%m.%Y')
    data['DATE_1'] = pd.to_datetime(data['DATE_1'], format='%d.%m.%Y')
    data['DIFF_NPR_DATE_DATE_1'] = data[['NPR_DATE','DATE_1']].apply(diff_dates, axis = 1)
    data['DATE_2'] = pd.to_datetime(data['DATE_2'], format='%d.%m.%Y')
    data['long_case'] = data['ED_COL'].map(lambda x: 1 if x>20 else 0)
    data['week_day_DATE_1'] = data['DATE_1'].dt.weekday
    data['week_day_DATE_2'] = data['DATE_2'].dt.weekday
    data.loc[data['FILENAME']=='D','P_CEL'] = data.loc[data['FILENAME']=='D','P_CEL'].fillna('Обращение с профилактической целью')
    
    # создаем словарь для преобразований
    values = {
            'DS0': 0,
            'DS2': 0,
            'DS3': 0,
            'GROUP_OMU': 'NO_OMU',
            'CRIT': 0,
            'P_CEL': 'Обращение по заболеванию',
            'CODE_USL': 'NO_USL',
            'SMO': 'MTR',
            'COUNTRY': 643
            }
    #заполняем оставшиеся записи константами в соответствии со словарем values
    data = data.fillna(values)
    
    convert_dict_PERSCODE = data.groupby(['PERSCODE'])['UUID'].count().to_dict()
    convert_dict_NHISTORY = data.groupby(['NHISTORY'])['UUID'].count().to_dict()

    data['number_of_cases'] = data['PERSCODE'].map(lambda x: convert_dict_PERSCODE.get(x,x))
    data['count_number_history'] = data['NHISTORY'].map(lambda x: convert_dict_NHISTORY.get(x,x))

    # создать признак **divergence_DS* -"расхождение направительного и основного диагнозов
    data['divergence_DS'] = data[['DS1','DS0']].apply(ds0_ds1, axis = 1) 
    
    # преобразуем признаки DS0, DS2, DS3, CRIT
    data['DS0'] = data['DS0'].apply(lambda x: 0 if x==0 else 1)
    data['DS2'] = data['DS2'].apply(lambda x: 0 if x==0 else 1)
    data['DS3'] = data['DS3'].apply(lambda x: 0 if x==0 else 1)
    data['CRIT'] = data['CRIT'].apply(lambda x: 0 if x==0 else 1)
    
    #Преобразуем **GROUP_OMU**, **DN**, **OKFS** в бинарные признаки.  
    data['GROUP_OMU'] = data['GROUP_OMU'].apply(lambda x: 0 if x=='NO_OMU' else 1).astype('int8')
    data['DN'] = data['DN'].apply(lambda x: 0 if x==0 else 1).astype('int8')
    data['OKFS'] = data['OKFS'].apply(lambda x: 1 if x==13 else 0).astype('int8')
        
    #Преобразуем **MO_level**, **VIDPOM**, **TYPE_MO**, **IDSP**, **P_CEL**, объединив редкие классы.
    data['MO_level'] = data['MO_level'].apply(lambda x: 1 if x==0 else x)
    data['VIDPOM'] = data['VIDPOM'].apply(lambda x: 31 if x==32 else x)
    data['VIDPOM'] = data['VIDPOM'].apply(lambda x: 13 if x==14 else x)
    data['TYPE_MO'] = data['TYPE_MO'].apply(lambda x: 'OTER' if x=='VED' else x)
    data['TYPE_MO'] = data['TYPE_MO'].apply(lambda x: 'OTER' if x=='FAP' else x)
    data['IDSP'] = data['IDSP'].apply(lambda x: 36 if x==24 else x)
    data['IDSP'] = data['IDSP'].apply(lambda x: 30 if x==32 else x)
    data['P_CEL'] = data['P_CEL'].apply(lambda x: 'Посещение по заболеванию' if x=='Aктивное посещение' else x)
    data['P_CEL'] = data['P_CEL'].apply(lambda x: 'Посещение по заболеванию' if x=='Посещениe в неотложной форме' else x)
    data['P_CEL'] = data['P_CEL'].apply(lambda x: 'Обращение с профилактической целью' if x=='Комплексное обследование' else x)
    data['P_CEL'] = data['P_CEL'].apply(lambda x: 'Обращение с профилактической целью' if x=='Патронаж' else x)
    
    #Удалим не нужные признаки
    drop_list = ['NPR_DATE', 'DATE_1', 'DATE_2', 'NHISTORY', 'PERSCODE','ED_COL']
    data = data.drop(drop_list, axis=1)
    
    return data

 
def df_predict_encoder(data):
    """ Функция для преобразования данных в датасет, 
    пригодный для подачи в модель для проведения 
    предсказания
    
    Args:
        - data: входной датасет
    Returns:
        - конвертированный датасет
    """
    data = convert_df(data)
    #Закодируем категориальные переменные *IDSP*, *VIDPOM*, *P_CEL*, *SMO*, *MO_level*, *C_ZAB*, 
    # *FOR_POM*, *USL_OK*, *FILENAME*, *divergence_DS*, *DIFF_NPR_DATE_DATE_1* унитарным кодом.
    data = pd.get_dummies(data, columns=['IDSP', 'VIDPOM', 'P_CEL', 'SMO', 'MO_level', 'C_ZAB',
                                         'FOR_POM', 'USL_OK', 'FILENAME', 'divergence_DS',
                                         'DIFF_NPR_DATE_DATE_1'], dtype='int8')
    
    data_skte_MEE = pd.DataFrame(skte_MEE.transform(data[col_list]), columns=skte_MEE.get_feature_names_out(skte_MEE.feature_names_in_))
    data_skte_EKMP = pd.DataFrame(skte_EKMP.transform(data[col_list]), columns=skte_EKMP.get_feature_names_out(skte_EKMP.feature_names_in_))
    del_list_c = []
    for col in data_skte_MEE.columns:
        if '_-1' in col:
            del_list_c.append(col)
        
    data_skte_MEE = data_skte_MEE.drop(del_list_c, axis = 1).astype('float32')
    data_skte_EKMP = data_skte_EKMP.drop(del_list_c, axis = 1).astype('float32')
    
    #Удалим не нужные столбцы, на основании которых были созданы новые переменные
    data.reset_index(inplace= True )
    data = data.drop(col_list+['index'], axis=1)
    
    # объединим основной датасет и датасет с созданными признаками
    data_MEE = pd.concat([data, data_skte_MEE], axis=1)
    data_EKMP = pd.concat([data, data_skte_EKMP], axis=1)
    data_MEE = add_columns_MEE(data_MEE)
    data_EKMP = add_columns_EKMP(data_EKMP)
    data_MEE = type_converter(data_MEE, columns_dict_trans_MEE)
    data_EKMP = type_converter(data_EKMP, columns_dict_trans_EKMP)
    convert_dict = {'float32': ['KOL_USL', 'ORIT', 'KD', 'AGE', 'TARIF', 'SUMV', 'attach', 'population']}
    data_MEE = type_converter(data_MEE, convert_dict)
    data_EKMP = type_converter(data_EKMP, convert_dict)

    num_transform = Pipeline(steps=[('qt', QuantileTransformer(n_quantiles=100, random_state=RANDOM_STATE))
                                ,('sc', MinMaxScaler())])
    data_MEE[num_cols_MEE] = num_transform.fit_transform(data_MEE[num_cols_MEE]).astype('float32')
    data_EKMP[num_cols_EKMP] = num_transform.fit_transform(data_EKMP[num_cols_EKMP]).astype('float32')
    data_MEE['KD']=np.log(data_MEE['KD']+0.1).astype('float32')
    data_EKMP['KD']=np.log(data_EKMP['KD']+0.1).astype('float32')
    
    return data_MEE, data_EKMP
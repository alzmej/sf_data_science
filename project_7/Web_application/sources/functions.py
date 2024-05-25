# Импорт необходимых библиотек
import pandas as pd
import numpy as np
from io import BytesIO
import xlsxwriter
import warnings
np.warnings = warnings
warnings.filterwarnings('ignore')


# фиксируем RANDOM_SEED
RANDOM_STATE = 42


def to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data


# функция для конвертации признаков
def group_omu_convert(item):
    """ Функция для конвертации значений GROUP_OMU
    
    Args:
        - item: значение поля для обработки
    Returns:
        - значение для нового признака
    """
    if ((item is np.nan) or (item == None)):
        return 'NO_OMU'
    if item in ['91','92','93']:
        return 8
    if item in ['98','99']:
        return 9
    else:
        return item[0]
    
    
def ds0_ds1(x):
    """ Функция для оценки расхождения диагнозов
    
    Args:
        - x: строка по отобранным столбцам датафрейма
    Returns:
        - значение для нового признака
    """
    if ((x['DS0'] is np.nan) or (x['DS0'] == None)):
        return -1
    if x['DS1']==x['DS0']:
        return 1
    else:
        return 0
    
    
def diff_dates(x):
    """ Функция для определения различия даты направления 
    на лечения и даты начала лечения
    
    Args:
        - x: строка по отобранным столбцам датафрейма
    Returns:
        - значение для нового признака
    """
    if x['NPR_DATE']==x['DATE_1']:
        return 0
    else:
        return 1
     
    
# функции для конвертации типов данных
def type_converter(df, columns_dict):
    """ Функция преобразующая типы данных датафрейма
    
    Args:
        - df: исходный датафрейм
        - columns_dict: словарь с ключами - целевыми типами данных
          и списками полей в качестве значений
    Returns:
        - датафрейм с изменениями
    """
    for item in columns_dict:
        for column in columns_dict[item]:
            df[column] = df[column].astype(item)
    return df


def trans_dict_gen(df,col_name=''):
    """ Функция формирующая справочник для конвертаци типов данных 
    
    Args:
        - df: исходный датафрейм
        - col_name: наименование колонки, котрую необходимо не включать в справочник
    Returns:
        - справочник вида "тип данных":[список колонок]
    """
    temp_dict = dict()
    all_columns = df.columns
    for column in all_columns:
        temp = []
        if column != col_name:
            col_type = str(df[column].dtypes)
            if temp_dict.get(col_type)==None:
                temp_dict[col_type] = [column]
            else:
                temp = temp_dict[col_type]
                temp.append(column)
                temp_dict[col_type] = temp
    return temp_dict

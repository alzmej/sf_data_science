import streamlit as st 
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from sources.connect import get_data
from sources.predict import predict_MEE, predict_EKMP, predict_all
from sources.converter import df_predict_encoder
from sources.functions import to_excel

st.set_page_config(page_title="Поиск дефектов медицинской помощи", page_icon="📊")
st.markdown(
    """
    Для оценки вероятности дефекта медицинской помощи
    по реестрам счетов необходимо выбрать параметры отбора случаев 
    и по полученному списку провести предсказание. Результат будет 
    выведен на экран в виде таблицы перечня случаев с вероятностью 
    необходимости проведения экспертизы МЭЭ и ЭКМП и вероятностью 
    соответствующего дефекта. Результат можно сохранить в файл 
    формата *.xlsx .
""")
predict_df = pd.DataFrame()
st.title('Предсказание дефектов случаев медпомощи')

with st.sidebar:
    med_test_radio = st.radio(
                            "Выберите вид отбора",
                            ["Год + месяц", "Год + месяц + код МО", "Год + месяц + код СМО",
                             "Год + месяц + код МО + код СМО", "Год + месяц + ФИО + ДР",
                             "Год + месяц + код МО + ФИО + ДР", "Год + месяц + код СМО + ФИО + ДР", 
                             "Год + месяц + код СМО + код МО + ФИО + ДР", "Год + месяц + ЕНП",
                             "Год + месяц + код МО + ЕНП", "Год + месяц + код СМО + ЕНП", 
                             "Год + месяц + код СМО + код МО + ЕНП"                        
                             ],
                        )
    st.write("Выбрана вид отбора:", med_test_radio)
    expertis_radio = st.radio('Выберите вид экспертизы',
                              ['MEE', 'EKMP', 'Всё'],
                              )
    year_radio = st.radio("Выберите отчётный год",
                          ['2023', '2024'],
                         )   
    month_radio = st.radio(
                            "Выберите отчётный месяц",
                            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                        )
    SMO_radio = st.radio(
                            "Выберите код СМО",
                            ['83001', '83005', '83008'],
                        )
    
    st.write("Выбран месяц ", month_radio, ' год ', year_radio)

if ((med_test_radio == "Год + месяц + код МО") or (med_test_radio == "Год + месяц + код МО + код СМО") or (med_test_radio == "Год + месяц + код МО + ФИО + ДР") 
    or (med_test_radio == "Год + месяц + код СМО + код МО + ФИО + ДР") or (med_test_radio == "Год + месяц + код МО + ЕНП") or (med_test_radio == "Год + месяц + код СМО + код МО + ЕНП")):
    MO_code = st.text_input("Введите MO код")
  
if ((med_test_radio == "Год + месяц + ФИО + ДР") or (med_test_radio == "Год + месяц + код СМО + ФИО + ДР") 
    or (med_test_radio == "Год + месяц + код МО + ФИО + ДР") or (med_test_radio == "Год + месяц + код СМО + код МО + ФИО + ДР")):
    FAM = st.text_input("Введите Фамилию")  
    IM = st.text_input("Введите Имя")
    OT = st.text_input("Введите Отчество")
    DR = st.date_input("Введите Дату рождения")
    
if ((med_test_radio == "Год + месяц + ЕНП") or (med_test_radio == "Год + месяц + код МО + ЕНП") or (med_test_radio == "Год + месяц + код СМО + ЕНП") 
    or (med_test_radio == "Год + месяц + код СМО + код МО + ЕНП")):
    ENP = st.text_input("Введите ENP")
    
if med_test_radio =='Год + месяц':
    argument=str('and s.YEAR = '+ year_radio +' and s.MONTH = '+ month_radio)
elif med_test_radio =="Год + месяц + код СМО":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.PLAT = ' + '\'' + str(SMO_radio) + '\'')
elif med_test_radio =="Год + месяц + код МО":    
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.CODE_MO = ' + '\'' + str(MO_code) + '\'')
elif med_test_radio =="Год + месяц + код МО + код СМО":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.PLAT = ' + '\'' + str(SMO_radio) + '\''+' and s.CODE_MO = ' + '\'' + str(MO_code) + '\'')    
elif med_test_radio =="Год + месяц + ФИО + ДР":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and sz.FAM = '+ '\'' + str(FAM) + '\'' +' and sz.IM = '+ '\''+ str(IM) + '\''+' and sz.OT = '+ '\''+ str(OT) + '\'' + ' and sz.DR = '+ '\''+ str(DR) + '\'')    
elif med_test_radio =="Год + месяц + код МО + ФИО + ДР":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.CODE_MO = ' + '\'' + str(MO_code) + '\'' +' and sz.FAM = '+ '\'' + FAM + '\'' +' and sz.IM = '+ '\''+ IM + '\''+' and sz.OT = '+ '\''+ OT + '\'' + ' and sz.DR = '+ '\''+ DR + '\'')
elif med_test_radio =="Год + месяц + код СМО + ФИО + ДР":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.PLAT = ' + '\'' + str(SMO_radio) + '\'' +' and sz.FAM = '+ '\'' + FAM + '\'' +' and sz.IM = '+ '\''+ IM + '\''+' and sz.OT = '+ '\''+ OT + '\'' + ' and sz.DR = '+ '\''+ DR + '\'')
elif med_test_radio =="Год + месяц + код СМО + код МО + ФИО + ДР":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.CODE_MO = ' + '\'' + str(MO_code) + '\'' +' and s.PLAT = ' + '\'' + str(SMO_radio) + '\'' +' and sz.FAM = '+ '\'' + FAM + '\'' +' and sz.IM = '+ '\''+ IM + '\''+' and sz.OT = '+ '\''+ OT + '\'' + ' and sz.DR = '+ '\''+ DR + '\'')
elif med_test_radio =="Год + месяц + ЕНП":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and sz.ENP = ' + '\'' + str(ENP) + '\'')
elif med_test_radio =="Год + месяц + код МО + ЕНП":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.CODE_MO = ' + '\'' + str(MO_code) + '\'' + ' and sz.ENP = ' + '\'' + str(ENP) + '\'')
elif med_test_radio =="Год + месяц + код СМО + ЕНП":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.PLAT = ' + '\'' + str(SMO_radio) + '\'' + ' and sz.ENP = ' + '\'' + str(ENP) + '\'')
elif med_test_radio =="Год + месяц + код СМО + код МО + ЕНП":
    argument=str('and s.YEAR = '+ str(year_radio) +' and s.MONTH = '+ str(month_radio) +' and s.CODE_MO = ' + '\'' + str(MO_code) + '\'' + ' and s.PLAT = ' + '\'' + str(SMO_radio) + '\'' + ' and sz.ENP = ' + '\'' + str(ENP) + '\'')

if st.button('Расчёт'):   
    df = get_data(argument)  
    temp_sluch_df = df[['UUID','ENP','FAM','IM','OT','BIRTHDAY','SMO','MO','VIDPOM','USL_OK','FOR_POM','PROFIL','DS1','NHISTORY','DATE_1','DATE_2','SUMV']]
    st.write('Данные успешно получены')
    st.write(df)    
    data_MEE, data_EKMP = df_predict_encoder(df)
    if expertis_radio=='MEE':
        predict_df = predict_MEE(data_MEE, temp_sluch_df)
        st.write('Предсказание выполнено')
        st.write(predict_df)
    elif expertis_radio=='EKMP':
        predict_df = predict_EKMP(data_EKMP, temp_sluch_df)
        st.write('Предсказание выполнено')
        st.write(predict_df)
    else:
        predict_df = predict_all(data_MEE, data_EKMP, temp_sluch_df)
        st.write('Предсказание выполнено')
        st.write(predict_df)
    
else:
    st.write('Выберите параметры и нажмите "Расчёт"')
    

df_xls = to_excel(predict_df)
st.download_button(label='📥 Сохранит результат',
                                data=df_xls ,
                                file_name= 'df_test.xlsx')
# Проект 8. Нахождения похожих товаров в интернет-магазинах по их описанию

## Оглавление  
[1. Описание проекта](https://github.com/alzmej/sf_data_science/tree/main/Project_8/README.md#Описание-проекта)  
[2. Какой кейс решаем?](https://github.com/alzmej/sf_data_science/tree/main/Project_8/README.md#Какой-кейс-решаем)  
[3. Краткая информация о данных](https://github.com/alzmej/sf_data_science/tree/main/Project_8/README.md#Краткая-информация-о-данных)  
[4. Результат](https://github.com/alzmej/sf_data_science/tree/main/Project_8/README.md#Результат)    
[5. Выводы](https://github.com/alzmej/sf_data_science/edit/main/Project_8/README.md#Выводы) 

### Описание проекта    
 По описанию одежды для активного отдыха найти похожую. Для решения задачи должно использоваться косинусное расстояние между веторами признаков описания.

:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/edit/main/Project_8/README.md#Оглавление)


### Какой кейс решаем?    
Для каждого id товара необходимо сформировать список id товаров, которые похожи на него 
  
:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/edit/main/Project_8/README.md#Оглавление)

### Краткая информация о данных
Датасет размещен в папке **data** [датасет](https://github.com/alzmej/sf_data_science/edit/main/Project_8/data/sample-data.csv)
И представлен 500 описаниями товаров.
  
:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/edit/main/Project_8/README.md#Оглавление)

### Результаты:  

В процессе работы проведены: 
1. Загрузка данных
2. Предварительная подготовка текста
3. Кластеризация при помощи методов TF-IDF, doc2vec, word2vec, DBSCAN
3. Рекомендация списков наиболее похожих товаров.

[ноутбук](https://github.com/alzmej/sf_data_science/edit/main/Project_8/nlp-boosting-online-sales-e-commerce.ipynb) с решением.

:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/tree/main/Project_8/README.md#Оглавление)


### Выводы:  

В зависимости от методики кластеризации списко рекомендаций несколько отличается, однако остается в целом релевантным с различными акцентами. В реальных условиях, вероятно нужно учитывать параметры кластериазции и особенности датасета, который не слишком велик для улавливания всех особенностей.

:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/tree/main/Project_8/README.md#Оглавление)


Если информация по этому проекту покажется вам интересной или полезной, то я буду очень вам благодарен, если отметите репозиторий и профиль ⭐️⭐️⭐️-дами

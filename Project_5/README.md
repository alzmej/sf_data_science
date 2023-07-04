# Проект 3. Предсказание рейтинга отеля по данным сайта Booking

## Оглавление  
[1. Описание проекта](https://github.com/alzmej/sf_data_science/tree/main/Project_5/README.md#Описание-проекта)  
[2. Какой кейс решаем?](https://github.com/alzmej/sf_data_science/tree/main/Project_5/README.md#Какой-кейс-решаем)  
[3. Краткая информация о данных](https://github.com/alzmej/sf_data_science/tree/main/Project_5/README.md#Краткая-информация-о-данных)  
[4. Результат](https://github.com/alzmej/sf_data_science/tree/main/Project_5/README.md#Результат)    
[5. Выводы](https://github.com/alzmej/sf_data_science/edit/main/Project_5/README.md#Выводы) 

### Описание проекта    
 Работая с датасетом, в котором содержатся сведения о 515 000 отзывов на отели Европы. Получить модель, которая должна предсказывать рейтинг отеля по данным сайта Booking на основе имеющихся в датасете данных. Задача решается в рамках участия в соревновании ["Прогнозирование рейтинга отеля на Booking"](https://www.kaggle.com/competitions/sf-booking) на площадке [Kaggle.com](https://www.kaggle.com/).

:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/edit/main/Project_5/README.md#Оглавление)


### Какой кейс решаем?    
Представьте, что вы работаете дата-сайентистом в компании Booking. Одна из проблем компании — это нечестные отели, которые накручивают себе рейтинг. Одним из способов обнаружения таких отелей является построение модели, которая предсказывает рейтинг отеля. Если предсказания модели сильно отличаются от фактического результата, то, возможно, отель ведёт себя нечестно, и его стоит проверить.

Вам поставлена задача создать такую модель. 
  
:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/edit/main/Project_5/README.md#Оглавление)

### Краткая информация о данных
Обучающий и тестовый [датасеты](https://www.kaggle.com/competitions/sf-booking/data) размещены в соревновании на [Kaggle.com](https://www.kaggle.com/). И представлены следующей структурой:
- *hotel_name* - название отеля;
- *hotel_address* - адрес отеля;
- *average_score* - средний балл отеля, рассчитанный на основе последнего комментария за последний год;
- *total_number_of_reviews* - общее количество действительных отзывов об отеле;
- *additional_number_of_scoring* - есть также некоторые гости, которые просто поставили оценку сервису, но не оставили отзыв. Это число указывает, сколько там действительных оценок без проверки.
- *lat* - географическая широта отеля;
- *lng* - географическая долгота отеля;
- *review_date* — дата, когда рецензент разместил соответствующий отзыв;
- *days_since_review* — количество дней между датой проверки и датой очистки;
- *negative_review* — отрицательный отзыв, который рецензент дал отелю;
- *review_total_negative_word_counts* — общее количество слов в отрицательном отзыв;
- *positive_review* — положительный отзыв, который рецензент дал отелю;
- *review_total_positive_word_counts* — общее количество слов в положительном отзыве.
- *reviewer_nationality* — страна рецензента;
- *total_number_of_reviews_reviewer_has_given* — количество отзывов, которые рецензенты дали в прошлом;
- *tags* — теги, которые рецензент дал отелю.
  
:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/edit/main/Project_5/README.md#Оглавление)

### Результаты:  

В процессе работы проведены: 
1. Загрузка и первичный анализ данных
2. Исследование и проектирование признаков
3. Очистка и отбор признаков
3. Обучение модели и получение предсказания

[Ноутбук с решением на Kaggle.com](https://www.kaggle.com/code/alexeytitarenko/booking-reviews-v1)

:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/tree/main/Project_5/README.md#Оглавление)


### Выводы:  

Признаки с большой степенью корреляции оказывают отрицательное значение и приводят к переобучению модели. Наибольшее значение для обучения модели имели признаки, связанные с отзывами путешественников, в меньшей степени признаки, основанные на разборе тегов, остальные признаки имеют меньшую значимость. Логарифмирование признаков не оказало значительного влияния на качество работы модели. За счёт удаления сильно коррелированных признаков удалось получить обучение модели с приемлемыми значениями метрики. 

В репозитории опубликован ноутбук с решением, в папке ["data"](https://github.com/alzmej/sf_data_science/tree/main/Project_5/data) вспомогательный датасет [new_zip_list.csv](https://github.com/alzmej/sf_data_science/tree/main/Project_5/data/new_zip_list.csv), файлы [requirements.txt](https://github.com/alzmej/sf_data_science/tree/main/Project_5/data/requirements.txt) и [submission.csv](https://github.com/alzmej/sf_data_science/tree/main/Project_5/data/submission.csv).

:arrow_up:[к оглавлению](https://github.com/alzmej/sf_data_science/tree/main/Project_5/README.md#Оглавление)


Если информация по этому проекту покажется вам интересной или полезной, то я буду очень вам благодарен, если отметите репозиторий и профиль ⭐️⭐️⭐️-дами

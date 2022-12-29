import numpy as np 

def game_core(number):
    '''Функция вычисляет загаданное число как точку на отрезке, используя алгоритм поиска минимума/максимума функции методом золотого сечения.
       Функция принимает загаданное число и возвращает число попыток.
       Сначала вычисляются стартовые значения, затем пошаговое приближение к загаданному числу.'''
    count = 1
    golden_ratio = 0.5 * (1 + 5**0.5)
    point_start = 0
    point_end = 100
    predict = round((point_start + point_end)/2)
    gold_point_2 = round(point_start + (point_end - point_start)/golden_ratio)
    gold_point_1 = round(point_end - (point_end - point_start)/golden_ratio)
    
    while number != predict:
        count+=1
        if number > gold_point_1: 
            point_start = gold_point_1   
            gold_point_1 = gold_point_2
            gold_point_2 = round(point_start + (point_end - point_start)/golden_ratio) 
        elif number < gold_point_2: 
            point_end = gold_point_2
            gold_point_2 = gold_point_1
            gold_point_1 = round(point_end - (point_end - point_start)/golden_ratio)
        predict = round((point_start + point_end)/2)       
    return(count) # выход из цикла, если угадали


def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))    
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)


if __name__ == "__main__":
    # RUN
    score_game(game_core)
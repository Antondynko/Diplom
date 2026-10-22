import numpy as np
import random
#np.random.seed(0)

def Generate_normal_matrix(n, m, l, h):
    # Генерируем матрицу из n строк и m столбцов с нормальным распределением
    mean = (l + h) / 2  # Среднее значение
    std_dev = (h - l) / 6  # Стандартное отклонение (чтобы 99.7% значений попали в диапазон [l, h])

    # Генерируем случайные значения из нормального распределения
    matrix = np.random.normal(mean, std_dev, (n, m))

    # Приводим значения к диапазону [l, h]
    matrix = np.clip(matrix, l, h)

    return matrix

def Generate_y_start(n, p):
    y_start = [0 for i in range(n)]
    indexes = [i for i in range(n)]

    indexes_one = random.sample(indexes, p)

    for i in indexes_one:
        y_start[i] = 1

    return y_start


n = 100  # количество строк.
m = 100  # количество столбцов
l_1 = 100 # нижняя граница диапазона
h_1 = 1000 # верхняя граница диапазона
l_2 = 1
h_2 = 10

#Транспортные расходы
c = Generate_normal_matrix(n, m, l_1, h_1)

#Предпочтения клиентов
d = Generate_normal_matrix(n, m, l_2, h_2)

#print(Generate_y_start(20, 15))
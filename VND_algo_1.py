import random
import import_from_file
import time

#const
INF = 2147483647

def Generate_y_start(n, p):
    """
    :param n: мощность множетсва I
    :param p: количество открываемых предприятий (медиана)
    :return: какое-то размещение, которое может быть решением задачи
    """
    y_start = [0 for i in range(n)]
    indexes = [i for i in range(n)]

    indexes_one = random.sample(indexes, p)

    for i in indexes_one:
        y_start[i] = 1

    return y_start

def Swap(y):
    """
    :param y: размещение, от которого строится окрестность
    :return: вектор из окретстности. Одно предприятие закрывается, а одно открывается.
    """

    # Вектор результата
    t = [0 for i in range(len(y))]

    zero = []
    one = []

    for i in range(len(y)):
        if y[i] == 0:
            zero.append(i)
        else:
            one.append(i)

    zero_x = random.choice(zero)
    one_x = random.choice(one)

    for i in range(len(y)):
        if i == zero_x:
            t[i] = 1
        else:
            if i == one_x:
                t[i] = 0
            else:
                t[i] = y[i]

    return t

def RhoC(x, c, V):
    """
    :param x: оптимальное решение задачи нижнего уровня
    :param c: матрица производственно-транспортных расходов
    :param V: порог
    :return: радиус пороговой устойчивости
    """
    m = len(x[0])
    n = len(x)
    f = 0
    rho = 0

    for i in range(n):
        for j in range(m):
            if x[i][j] == 1:
                f += c[i][j]


    rho = (V - f)/m
    return rho

def XC(y, d):
    """
    :param y: решение Лидера: размещени
    :param d: матрица предпочтений клиентов
    :return: матрица клиентов, решение задачи нижнего уровня
    """
    n = len(d)
    m = len(d[0])
    x = [[0 for i in range(m)] for i in range(n)]

    for i in range(m):
        indx = 0
        min = INF
        for j in range(n):
            if d[j][i] < min and y[j] == 1:
                indx = j
                min = d[j][i]

        x[indx][i] = 1

    return x

def Neighborhood_search(y_start, opt_start):
    """
    :param y_start: размещение
    :param opt_start: радиус пороговой устойчивости на этом размещении
    :return: размещение, которое в окрестности swap(y) будет давать лучший результат
    """
    vector_opt = y_start
    local_opt = opt_start
    iteration = p * (n - p)

    #print("в начальном размещении:", vector_opt)
    #print("значение целевой функции =",  local_opt)

    for i in range(iteration):
        vector = Swap(y_start)
        if RhoC(XC(vector, d), c, V) > local_opt:
            local_opt = RhoC(XC(vector, d), c, V)
            vector_opt = vector

    #print("оптимально значение целевой функции в окрестности =", local_opt)
    #print("оно достигается на векторе:", vector_opt)
    return vector_opt

def K_swap(y, k):
    """
    :param y: вектор размещения
    :param k: ранг окрестности
    :return:
    """
    # Проверяем, чтобы массив содержал как минимум 2 элемента
    if sum(y) < k:
        raise ValueError("k!")

    indexes_one = []
    indexes_zero = []

    for i in range(len(y)):
        if y[i] == 1:
            indexes_one.append(i)
        else:
            indexes_zero.append(i)

    # Выбираем два различных случайных элемента
    a = random.sample(indexes_one, k)
    b = random.sample(indexes_zero, k)

    result_y = y
    for i in a:
        result_y[i] = 0

    for i in b:
        result_y[i] = 1

    return result_y

#----------------------- Data -----------------------

start_time = time.time()

V = 18187.112199943476
p = 15
n = import_from_file.n
m = import_from_file.m

c = import_from_file.c
d = import_from_file.d

y_start = Generate_y_start(n, p)

rho = 0
opt = [0 for i in range(n)]

#----------------------- Local-Search second generation -----------------------
vector_opt = Neighborhood_search(y_start, RhoC(XC(y_start, d), c, V))
local_opt = RhoC(XC(vector_opt, d), c, V)

print("Изначальное размещение:", y_start)
print("rho =", RhoC(XC(y_start, d), c, V))
print("Размещение оптимальное в окрестности:", vector_opt)
print("rho =", local_opt)

for i in range(20):
    vector = Neighborhood_search(vector_opt, local_opt)
    current_opt = RhoC(XC(vector, d), c, V)
    if current_opt > local_opt:
        vector_opt = vector
        local_opt = current_opt

rho = local_opt
opt = vector_opt

print("Размещение после процедуры локального спуска:", opt)
print("rho =", rho)


#----------------------- Improve - global optimum -----------------------
l = 0
while True:
    if l >= 100:
        print("Улучшения целевой функции не зафиксировано.")
        break

    vector_curr = K_swap(vector_opt, 2)
    opt_curr = RhoC(XC(vector_curr, d), c, V)

    if opt_curr > local_opt:
        print("Локальный оптимум, не является глобальным!")
        print("Новое размещение:", vector_curr)
        print("Значение целевой функции =", opt_curr)
        local_opt = opt_curr
        vector_opt = vector_curr
        break

    l += 1

print("_____Solution____")
print("Радиус пороговой устойчивости =", rho)

end_time = time.time()
elapsed_time = end_time - start_time
print('Время работы алгоритма: ', elapsed_time)

print(RhoC(XC([0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0], d), c, V))
import import_from_file
import random
import time

# const
INF = 2147483647

# time
start_time = time.time()

def Generate_y_start(n, p):
    y_start = [0 for i in range(n)]
    indexes = [i for i in range(n)]

    indexes_one = random.sample(indexes, p)

    for i in indexes_one:
        y_start[i] = 1

    return y_start

def XC(y, d):
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

def VC(x, c):
    m = len(x[0])
    n = len(x)
    V = 0

    for i in range(n):
        for j in range(m):
            if x[i][j] == 1:
                V += c[i][j]
    return V

def Neighborhood_search(y_start, opt_start):
    vector_opt = y_start
    local_opt = opt_start
    iteration = p * (n - p)

    #print("в начальном размещении:", vector_opt)
    #print("значение целевой функции =",  local_opt)

    for i in range(iteration):
        vector = Swap(y_start)
        if VC(XC(vector, d), c) < local_opt:
            local_opt = VC(XC(vector, d), c)
            vector_opt = vector

    #print("оптимально значение целевой функции в окрестности =", local_opt)
    #print("оно достигается на векторе:", vector_opt)
    return vector_opt

def Swap(y):

  '''
  Функция возвращающая вектор из окрестности swap, заданного вектора.
  Организация окрестностной структуры - мы создаем вектор из окрестности swap.
  Одно предприятие закрывается, а одно открывается.
  '''

  # array of result vectors from swap
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

def K_swap(y, k):
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

def RhoC(x, c, V):
    m = len(x[0])
    n = len(x)
    C = 0

    for i in range(n):
        for j in range(m):
            if x[i][j] == 1:
                C += c[i][j]

    rho = (V - C)/m
    return rho


# Data
p = 15
n = import_from_file.n
m = import_from_file.m

c = import_from_file.c
d = import_from_file.d

# Start y
y_start = [0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1] #Generate_y_start(n, p)

V = 0
opt = [0 for i in range(n)]

#----------------------- Local-Search second generation -----------------------
vector_opt = Neighborhood_search(y_start, VC(XC(y_start, d), c))
local_opt = VC(XC(vector_opt, d), c)

print("Изначальное размещение:", y_start, "V =", VC(XC(y_start, d), c))
print("Размещение оптимальное в окрестности:", vector_opt, "V =", local_opt)

for i in range(20):
    vector = Neighborhood_search(vector_opt, local_opt)
    current_opt = VC(XC(vector, d), c)
    if current_opt < local_opt:
        vector_opt = vector
        local_opt = current_opt

V = local_opt
opt = [0 for i in range(len(vector_opt))]

for i in range(len(vector_opt)):
    if vector_opt[i] == 1:
        opt[i] = 1



print("Размещение после процедуры локального спуска:", opt)
print("Значение целевой функции =", V)


#----------------------- Shake - global optimum -----------------------
l = 0
while True:
    if l >= 100:
        print("Улучшения целевой функции не зафиксировано.")
        break

    vector_curr = K_swap(vector_opt, 2)
    opt_curr = VC(XC(vector_curr, d), c)

    if opt_curr < local_opt:
        print("Локальный оптимум, не является глобальным!")
        print("Новое размещение:", vector_curr)
        print("Значение целевой функции =", opt_curr)
        local_opt = opt_curr
        vector_opt = vector_curr
        break

    l += 1

print("_____Solution____")
print("Значение целевой функции =", V)
print("Достигнуто на размещении: ", opt)
# Warning!
print("rho на этом размещении: ", RhoC(XC(opt, d), c, V * 1.2))

end_time = time.time()
elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)
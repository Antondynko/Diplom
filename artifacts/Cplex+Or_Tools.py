from ortools.linear_solver import pywraplp

import import_from_file
import time


start_time = time.time()

solver = pywraplp.Solver.CreateSolver('SCIP')

if not solver:
    print('Не удалось создать решатель Cplex.')
else:
    print('Решатель SCIP успешно подключен и запущен.')

n = import_from_file.n
m = import_from_file.m

I = [i for i in range(n)]  # Набор i (например, центры)
J = [i for i in range(m)]  # Набор j (например, клиенты)
c = import_from_file.c
d = import_from_file.d
p = 15 # Количество центров
V = 11436

# Объявляем переменные
x = {}
for i in I:
    for j in J:
        x[i, j] = solver.BoolVar(f'x_{i}_{j}')

y = {}
for i in I:
    y[i] = solver.BoolVar(f'y_{i}')

z = {}
for k in I:
    for i in I:
        for j in J:
            z[k, i, j] = solver.BoolVar(f'z_{k}_{i}_{j}')

rho = solver.NumVar(0, solver.infinity(), 'rho')

# Целевая функция
solver.Maximize(rho)

# Ограничения
for j in J:
    solver.Add(sum(x[i, j] for i in I) == 1)

solver.Add(sum(y[i] for i in I) == p)

solver.Add(sum(sum((c[i][j] * x[i, j]) for j in J) for i in I) + m * rho <= V)

for j in J:
    for k in I:
        for i in I:
            solver.Add(z[k, i, j] <= x[i, j])

for j in J:
    for k in I:
        for i in I:
            solver.Add(z[k, i, j] <= y[k])

for j in J:
    for k in I:
        for i in I:
            solver.Add(x[i, j] + y[k] - z[k, i, j] <= 1)

for j in J:
    for k in I:
        solver.Add(sum(d[i][j] * z[k, i, j] for i in I) <= d[k][j] * y[k])

for i in I:
  for j in J:
    solver.Add(x[i, j] <= y[i])

# Оптимизация
status = solver.Solve()

result_vector = [0 for i in range(n)]

# Вывод результатов
if status == pywraplp.Solver.OPTIMAL:
    print(f"Optimal rho: {rho.solution_value()}")
    for i in I:
        for j in J:
            if x[i, j].solution_value() > 0.5:
                print(f"Client {j} assigned to center {i}")
    for i in I:
        if y[i].solution_value() > 0.5:
            result_vector[i] = 1
            print(f"Center {i} is open")
else:
    print("No optimal solution found.")

print(result_vector)

end_time = time.time()
elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)

# 20_20_15
#
#
#

# 20_20_5
# opt = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1] = 179.87799621886472 (RhoC = -43.86159270905991)
# Vnd = [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0] = 15.94202989956184
# delta = 163.93596631930288

#20_20_10
# opt = [0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1] = 317.6160214448081 (RhoC = 32.625937903252634)
# Vnd = [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1] = 101.23456349538328
# delta = 216.38145794942483

# 5_10_2
# opt = [0, 0, 1, 0, 1] = 624.7811723736392 (RhoC = 479.20012178211374)
# Vnd = [0, 0, 0, 1, 1] = 521.282487087002
# delta = 103.49868528663717

# 40_40_10
# opt = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0,
# 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0] - 2235.7549141203076
# Vnd = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0,
# 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0] - 2083.0488285073416
#
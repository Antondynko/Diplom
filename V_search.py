from ortools.linear_solver import pywraplp
import import_from_file
import time

start_time = time.time()

solver = pywraplp.Solver.CreateSolver('SCIP')

if not solver:
    print('Не удалось создать решатель SCIP.')
else:
    print('Решатель SCIP успешно подключен и запущен.')

# Data

n = import_from_file.n
m = import_from_file.m

I = [i for i in range(n)]  # Набор i (например, центры)
J = [i for i in range(m)]  # Набор j (например, клиенты)
c = import_from_file.c
d = import_from_file.d
p = 15 # Количество центров

# Data

# Checking

print(n)
print(m)
print(c[0][0])
print(d[0][0])

# Checking


#Variables
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



# Целевая функция
solver.Minimize(sum(sum(c[i][j] * x[i, j] for j in range(m)) for i in range(n)))

# Ограничения
for j in J:
    solver.Add(sum(x[i, j] for i in I) == 1)

solver.Add(sum(y[i] for i in I) == p)

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

for i in I:
  for j in J:
    solver.Add(x[i, j] <= y[i])

for j in J:
    for k in I:
        solver.Add(sum(d[i][j] * z[k, i, j] for i in I) <= d[k][j] * y[k])

# Оптимизация
status = solver.Solve()

result_vector = [0 for i in range(n)]

# Вывод результатов
if status == pywraplp.Solver.OPTIMAL:
    V = 0
    for i in range(n):
        for j in range(m):
            V += c[i][j]* x[i, j].solution_value()
    for i in I:
        for j in J:
            if x[i, j].solution_value() > 0.5:
                print(f"Client {j} assigned to center {i}")
    for i in I:
        if y[i].solution_value() > 0.5:
            result_vector[i] = 1
            print(f"Center {i} is open")

    print("Solution: V =", V)
else:
    print("No optimal solution found.")

print("Solution vector:", result_vector)

end_time = time.time()
elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)
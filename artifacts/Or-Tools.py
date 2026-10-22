from ortools.linear_solver import pywraplp
import Data_generate

'''
# Function converting a list of strings into a list of integers
def int_list(a):
  count = 0
  for i in range(len(a)):
    count = int(a[i])
    a[i] = count
  return a

n = 100
p = 14

f = open('333Bi_GapC.txt', 'r')

lines = []
count = []

for line in f:
  lines.append(line)

for i in range(4, len(lines)):
  count = lines[i].split()
  lines[i] = int_list(count)

f.close

# Data: list of Transportation Cost
c = [[99 for j in range(n)] for i in range(n)]

# Data: Preference
d = [[99 for j in range(n)] for i in range(n)]


for i in range(4, len(lines)):
  t = lines[i]
  c[t[0] - 1][t[1] - 1] = t[2]
  d[t[0] - 1][t[1] - 1] = t[3]

c_d = {}
d_d = {}

for i in range(1, len(c) + 1):
  for j in range(1, len(c[i - 1]) + 1):
    cup = (i, j)
    c_d[cup] = c[i - 1][j - 1]

for i in range(1, len(d) + 1):
  for j in range(1, len(d[i - 1]) + 1):
    dup = (i, j)
    d_d[dup] = d[i - 1][j - 1]

print(d_d[(1, 28)])
'''

# Данные
I = [i for i in range(1, 101)]  # Набор i (например, центры)
J = [i for i in range(1, 101)]  # Набор j (например, клиенты)
c = c_d
d = d_d
p = 14  # Количество центров
V = 1000  # Ограничение на общую стоимость
m = len(J) # Количество клиентов

# Модель
solver = pywraplp.Solver.CreateSolver('SCIP')

# Переменные
x = {}
for i in I:
    for j in J:
        x[i, j] = solver.BoolVar(f'x_{i}_{j}')
y = {}
for i in I:
    y[i] = solver.BoolVar(f'y_{i}')
rho = solver.NumVar(0, solver.infinity(), 'rho')

# Целевая функция
solver.Maximize(rho)

# Ограничения
# (19) Каждому клиенту назначен только один центр
for j in J:
    solver.Add(sum(x[i, j] for i in I) == 1)

# (18) Общее количество открытых центров равно p
solver.Add(sum(y[i] for i in I) == p)

# (16) Ограничение стоимости
solver.Add(sum(sum((c[i, j] * x[i, j]) for j in J) for i in I) + m * rho <= V)

# (17) Ограничение расстояния
for j in J:
    for i in I:
        solver.Add(d[i, j] * x[i, j] <= sum(d[k, j] * y[k] for k in I))

# (18) Ограничение
for i in I:
  for j in J:
    solver.Add(x[i, j] <= y[i])

# Оптимизация
status = solver.Solve()

# Вывод результатов
if status == pywraplp.Solver.OPTIMAL:
    print(f"Optimal rho: {rho.solution_value()}")
    for i in I:
        for j in J:
            if x[i, j].solution_value() > 0.5:
                print(f"Client {j} assigned to center {i}")
    for i in I:
        if y[i].solution_value() > 0.5:
            print(f"Center {i} is open")
else:
    print("No optimal solution found.")
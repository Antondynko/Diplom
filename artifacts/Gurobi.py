from gurobipy import Model, GRB, quicksum
import import_from_file
import time

start_time = time.time()

# Данные
n = import_from_file.n
m = import_from_file.m

I = [i for i in range(n)]  # Набор i (центры)
J = [i for i in range(m)]  # Набор j (клиенты)

c = import_from_file.c
d = import_from_file.d

p = 15  # Количество центров
V = 16000 # Ограничение на общую стоимость

# Модель
model = Model("Optimization")


# Переменные
x = model.addVars(I, J, vtype=GRB.BINARY, name="x")
y = model.addVars(I, vtype=GRB.BINARY, name="y")
rho = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="rho")
z = model.addVars(I, I, J, vtype=GRB.BINARY, name="z")

# Целевая функция
model.setObjective(rho, GRB.MAXIMIZE)

# Ограничения
model.addConstrs((sum(x[i, j] for i in I) == 1 for j in J), "AssignEachJ")  # (20)
model.addConstr(sum(y[i] for i in I) == p, "NumberOfCenters")  # (18)
model.addConstr(sum(sum((c[i][j] * x[i, j]) for j in J) for i in I) + m * rho <= V, "CostConstraint")  # (16)

model.addConstrs(z[k, i, j] <= x[i, j] for k in I for i in I for j in J)
model.addConstrs(z[k, i, j] <= y[k] for k in I for i in I for j in J)
model.addConstrs(x[i, j] + y[k] - z[k, i, j] <= 1 for k in I for i in I for j in J)
model.addConstrs(sum(d[i][j] * z[k, i, j] for i in I) <= d[k][j] * y[k] for j in J for k in I)

model.addConstrs(x[i, j] <= y[i] for i in I for j in J)

model.setParam('TimeLimit', 10800)

# Оптимизация
model.optimize()


# Вывод результатов
result_vector = [0 for i in range(n)]
result_matrix = [[0 for i in range(m)] for i in range(n)]

if model.status == GRB.OPTIMAL:
    print(f"Optimal rho: {rho.x}")
    for i in I:
        for j in J:
            if x[i, j].x > 0.5:
                print(f"Client {j} assigned to center {i}")
                result_matrix[i][j] = 1
    for i in I:
        if y[i].x > 0.5:
            result_vector[i] = 1
            print(f"Center {i} is open")
else:
    if model.status == GRB.Status.TIME_LIMIT:
        if model.SolCount > 1:
            print("Достигнут лимит времени. Найдено допустимое решение.")
            print(f"Optimal rho: {rho.x}")
            for i in I:
                for j in J:
                    if x[i, j].x > 0.5:
                        print(f"Client {j} assigned to center {i}")
                        result_matrix[i][j] = 1
            for i in I:
                if y[i].x > 0.5:
                    result_vector[i] = 1
                    print(f"Center {i} is open")
        else:
            print("No feasible solution found.")
    else:
        print("No optimal solution found.")

print("_____Solution_____")
print("HIGH LEVEL - Solution vector:", result_vector)
print("LOW LEVEL - Solution matrix:")
for i in range(n):
    print(result_matrix[i])

end_time = time.time()
elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)

# gurobi [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]
# scip   [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]

# [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
from gurobipy import Model, GRB
import import_from_file
import time

# Timing
start_time = time.time()

# Data
n = import_from_file.n
m = import_from_file.m

I = [i for i in range(n)]  # Набор i (например, центры)
J = [i for i in range(m)]  # Набор j (например, клиенты)
c = import_from_file.c
d = import_from_file.d
p = 15 # Количество центров

# Model
model = Model("Optimization")

# Variables

x = model.addVars(I, J, vtype=GRB.BINARY, name="x")
y = model.addVars(I, vtype=GRB.BINARY, name="y")
z = model.addVars(I, I, J, vtype=GRB.BINARY, name="z")

# Objective function
model.setObjective(sum(sum(c[i][j] * x[i, j] for j in range(m)) for i in range(n)), GRB.MINIMIZE)

# Constr
model.addConstrs((sum(x[i, j] for i in I) == 1 for j in J))
model.addConstr(sum(y[i] for i in I) == p)

model.addConstrs(z[k, i, j] <= x[i, j] for k in I for i in I for j in J)
model.addConstrs(z[k, i, j] <= y[k] for k in I for i in I for j in J)
model.addConstrs(x[i, j] + y[k] - z[k, i, j] <= 1 for k in I for i in I for j in J)
model.addConstrs(sum(d[i][j] * z[k, i, j] for i in I) <= d[k][j] * y[k] for j in J for k in I)

model.addConstrs(x[i, j] <= y[i] for i in I for j in J)

model.setParam('TimeLimit', 3600)

# Optimize`
model.optimize()

# Result
result_vector = [0 for i in range(n)]
result_matrix = [[0 for i in range(m)] for i in range(n)]

if model.status == GRB.OPTIMAL:
    V = 0
    for i in range(n):
        for j in range(m):
            V += c[i][j] * x[i, j].X
    for i in I:
        for j in J:
            if x[i, j].X > 0.5:
                print(f"Client {j} assigned to center {i}")
                result_matrix[i][j] = 1
    for i in I:
        if y[i].X > 0.5:
            result_vector[i] = 1
            print(f"Center {i} is open")

    print("Optimal: V =", V)
else:
    if model.status == GRB.Status.TIME_LIMIT:
        print("Достигнут лимит времени. Найдено допустимое решение.")
        V = 0
        for i in range(n):
            for j in range(m):
                V += c[i][j] * x[i, j].X
        for i in I:
            for j in J:
                if x[i, j].X > 0.5:
                    print(f"Client {j} assigned to center {i}")
                    result_matrix[i][j] = 1
        for i in I:
            if y[i].X > 0.5:
                result_vector[i] = 1
                print(f"Center {i} is open")

        print("Optimal: V =", V)
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

# ___Scip___
# Solution: V = 10396.575685420508
# Solution vector: [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]
# ___Gurobi___
# Solution: V = 10396.575685420508
# Solution vector: [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]

#___Gurobi___
# 40_100_5.txt
# Solution: V = 48992.20820364008
# Solution vector: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
# Elapsed time:  23153.832674264908
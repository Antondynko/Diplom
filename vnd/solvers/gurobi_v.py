"""MIP: min cost (поиск V) при заданном p (Gurobi).

Запуск: python -m vnd.solvers.gurobi_v --data datasets/30_30_15.txt --p 15
"""

import argparse
import time

from gurobipy import GRB, Model

from vnd.data import load_dataset


def solve(problem, p: int, time_limit: float = 3600.0) -> tuple[float, list[int]]:
    """Решает вводную задачу: min Σc·x (Gurobi).

    :return: (V, y)
    """
    n, m = problem.n, problem.m
    c, d = problem.c, problem.d

    model = Model("Optimization")
    model.setParam("TimeLimit", time_limit)

    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")
    y = model.addVars(n, vtype=GRB.BINARY, name="y")
    z = model.addVars(n, n, m, vtype=GRB.BINARY, name="z")

    model.setObjective(
        sum(c[i][j] * x[i, j] for i in range(n) for j in range(m)), GRB.MINIMIZE
    )

    model.addConstrs((sum(x[i, j] for i in range(n)) == 1 for j in range(m)))
    model.addConstr(sum(y[i] for i in range(n)) == p)

    model.addConstrs(z[k, i, j] <= x[i, j] for k in range(n) for i in range(n) for j in range(m))
    model.addConstrs(z[k, i, j] <= y[k] for k in range(n) for i in range(n) for j in range(m))
    model.addConstrs(x[i, j] + y[k] - z[k, i, j] <= 1 for k in range(n) for i in range(n) for j in range(m))
    model.addConstrs(sum(d[i][j] * z[k, i, j] for i in range(n)) <= d[k][j] * y[k] for k in range(n) for j in range(m))
    model.addConstrs(x[i, j] <= y[i] for i in range(n) for j in range(m))

    model.optimize()

    y_vec = [0] * n
    V_val = float("inf")

    if model.status in (GRB.OPTIMAL, GRB.Status.TIME_LIMIT) and model.SolCount > 0:
        V_val = model.ObjVal
        for i in range(n):
            if y[i].X > 0.5:
                y_vec[i] = 1

    return V_val, y_vec


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIP: min cost / V (Gurobi)")
    parser.add_argument("--data", required=True, help="Путь к файлу данных")
    parser.add_argument("--p", type=int, required=True, help="Количество центров")
    parser.add_argument("--time-limit", type=float, default=3600.0, help="Лимит времени (сек)")
    args = parser.parse_args()

    problem = load_dataset(args.data)
    start = time.time()

    V_val, y_vec = solve(problem, args.p, args.time_limit)

    print(f"Optimal V: {V_val:.4f}")
    print("Solution vector:", y_vec)
    print("Elapsed: {:.2f}s".format(time.time() - start))

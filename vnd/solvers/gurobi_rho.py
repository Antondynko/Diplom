"""MIP: max ρ при заданном V и p (Gurobi).

Запуск: python -m vnd.solvers.gurobi_rho --data datasets/30_30_15.txt --p 15 --V 16000
"""

import argparse
import time

from gurobipy import GRB, Model

from vnd.data import load_dataset


def solve(problem, p: int, V: float, time_limit: float = 10800.0) -> tuple[float, list[int], list[list[int]]]:
    """Решает основную задачу на Gurobi.

    :return: (rho, y, x)
    """
    n, m = problem.n, problem.m
    c, d = problem.c, problem.d

    model = Model("Optimization")
    model.setParam("TimeLimit", time_limit)

    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")
    y = model.addVars(n, vtype=GRB.BINARY, name="y")
    rho = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="rho")
    z = model.addVars(n, n, m, vtype=GRB.BINARY, name="z")

    model.setObjective(rho, GRB.MAXIMIZE)

    model.addConstrs((sum(x[i, j] for i in range(n)) == 1 for j in range(m)), "AssignEachJ")
    model.addConstr(sum(y[i] for i in range(n)) == p, "NumberOfCenters")
    model.addConstr(sum(c[i][j] * x[i, j] for i in range(n) for j in range(m)) + m * rho <= V, "CostConstraint")

    model.addConstrs(z[k, i, j] <= x[i, j] for k in range(n) for i in range(n) for j in range(m))
    model.addConstrs(z[k, i, j] <= y[k] for k in range(n) for i in range(n) for j in range(m))
    model.addConstrs(x[i, j] + y[k] - z[k, i, j] <= 1 for k in range(n) for i in range(n) for j in range(m))
    model.addConstrs(sum(d[i][j] * z[k, i, j] for i in range(n)) <= d[k][j] * y[k] for k in range(n) for j in range(m))
    model.addConstrs(x[i, j] <= y[i] for i in range(n) for j in range(m))

    model.optimize()

    y_vec = [0] * n
    x_mat = [[0] * m for _ in range(n)]
    rho_val = float("-inf")

    if model.status in (GRB.OPTIMAL, GRB.Status.TIME_LIMIT) and model.SolCount > 0:
        rho_val = rho.X
        for i in range(n):
            for j in range(m):
                if x[i, j].X > 0.5:
                    x_mat[i][j] = 1
            if y[i].X > 0.5:
                y_vec[i] = 1

    return rho_val, y_vec, x_mat


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIP: max rho (Gurobi)")
    parser.add_argument("--data", required=True, help="Путь к файлу данных")
    parser.add_argument("--p", type=int, required=True, help="Количество центров")
    parser.add_argument("--V", type=float, required=True, help="Бюджет")
    parser.add_argument("--time-limit", type=float, default=10800.0, help="Лимит времени (сек)")
    args = parser.parse_args()

    problem = load_dataset(args.data)
    start = time.time()

    rho_val, y_vec, x_mat = solve(problem, args.p, args.V, args.time_limit)

    print(f"Optimal rho: {rho_val:.4f}")
    print("Solution vector:", y_vec)
    print("Elapsed: {:.2f}s".format(time.time() - start))

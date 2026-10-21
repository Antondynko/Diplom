"""MIP: min cost (поиск V) при заданном p (SCIP через OR-Tools).

Запуск: python -m vnd.solvers.scip_v --data datasets/30_30_15.txt --p 15
"""

import argparse
import time

from ortools.linear_solver import pywraplp

from vnd.data import load_dataset


def solve(problem, p: int) -> tuple[float, list[int]]:
    """Решает вводную задачу: min Σc·x (SCIP).

    :return: (V, y)
    """
    n, m = problem.n, problem.m
    c, d = problem.c, problem.d

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        raise RuntimeError("Не удалось создать решатель SCIP")

    x = {}
    for i in range(n):
        for j in range(m):
            x[i, j] = solver.BoolVar(f"x_{i}_{j}")
    y = {}
    for i in range(n):
        y[i] = solver.BoolVar(f"y_{i}")
    z = {}
    for k in range(n):
        for i in range(n):
            for j in range(m):
                z[k, i, j] = solver.BoolVar(f"z_{k}_{i}_{j}")

    solver.Minimize(
        sum(c[i][j] * x[i, j] for i in range(n) for j in range(m))
    )

    for j in range(m):
        solver.Add(sum(x[i, j] for i in range(n)) == 1)

    solver.Add(sum(y[i] for i in range(n)) == p)

    for j in range(m):
        for k in range(n):
            for i in range(n):
                solver.Add(z[k, i, j] <= x[i, j])
                solver.Add(z[k, i, j] <= y[k])
                solver.Add(x[i, j] + y[k] - z[k, i, j] <= 1)

    for k in range(n):
        for j in range(m):
            solver.Add(
                sum(d[i][j] * z[k, i, j] for i in range(n)) <= d[k][j] * y[k]
            )

    for i in range(n):
        for j in range(m):
            solver.Add(x[i, j] <= y[i])

    status = solver.Solve()

    y_vec = [0] * n
    V_val = float("inf")

    if status == pywraplp.Solver.OPTIMAL:
        V_val = solver.ObjectiveValue()
        for i in range(n):
            if y[i].solution_value() > 0.5:
                y_vec[i] = 1

    return V_val, y_vec


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIP: min cost / V (SCIP)")
    parser.add_argument("--data", required=True, help="Путь к файлу данных")
    parser.add_argument("--p", type=int, required=True, help="Количество центров")
    args = parser.parse_args()

    problem = load_dataset(args.data)
    start = time.time()

    V_val, y_vec = solve(problem, args.p)

    print(f"Optimal V: {V_val:.4f}")
    print("Solution vector:", y_vec)
    print("Elapsed: {:.2f}s".format(time.time() - start))

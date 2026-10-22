"""MIP: max ρ при заданном V и p (Cplex через OR-Tools).

Запуск: python -m vnd.solvers.cplex_rho --data datasets/30_30_15.txt --p 15 --V 16000
"""

import argparse
import time

from ortools.linear_solver import pywraplp

from vnd.data import load_dataset


def solve(problem, p: int, V: float) -> tuple[float, list[int]]:
    """Решает основную задачу на Cplex.

    :return: (rho, y)
    """
    n, m = problem.n, problem.m
    c, d = problem.c, problem.d

    solver = pywraplp.Solver.CreateSolver("CPLEX")
    if solver is None:
        raise RuntimeError("Не удалось создать решатель Cplex")

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
    rho = solver.NumVar(0, solver.infinity(), "rho")

    solver.Maximize(rho)

    for j in range(m):
        solver.Add(sum(x[i, j] for i in range(n)) == 1)

    solver.Add(sum(y[i] for i in range(n)) == p)

    solver.Add(
        sum(c[i][j] * x[i, j] for i in range(n) for j in range(m)) + m * rho <= V
    )

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
    rho_val = float("-inf")

    if status == pywraplp.Solver.OPTIMAL:
        rho_val = rho.solution_value()
        for i in range(n):
            if y[i].solution_value() > 0.5:
                y_vec[i] = 1

    return rho_val, y_vec


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIP: max rho (Cplex)")
    parser.add_argument("--data", required=True, help="Путь к файлу данных")
    parser.add_argument("--p", type=int, required=True, help="Количество центров")
    parser.add_argument("--V", type=float, required=True, help="Бюджет")
    args = parser.parse_args()

    problem = load_dataset(args.data)
    start = time.time()

    rho_val, y_vec = solve(problem, args.p, args.V)

    print(f"Optimal rho: {rho_val:.4f}")
    print("Solution vector:", y_vec)
    print("Elapsed: {:.2f}s".format(time.time() - start))

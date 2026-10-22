"""Legacy: VND с рандомным 1-swap + K_swap (2-swap), max ρ.

Логика — из VND_algo_1.py. Использует общие функции из vnd/.
Запуск: python -m vnd.heuristic.vnd_legacy_1 --data datasets/30_30_15.txt --p 15 --V 16000
"""

import argparse
import random
import time

from vnd.data import load_dataset
from vnd.model import rc
from vnd.neighborhoods import generate_y_start


def random_swap(y: list[int]) -> list[int]:
    """Один случайный 1-swap."""
    one = [i for i in range(len(y)) if y[i] == 1]
    zero = [i for i in range(len(y)) if y[i] == 0]
    v = list(y)
    v[random.choice(one)] = 0
    v[random.choice(zero)] = 1
    return v


def k_swap(y: list[int], k: int) -> list[int]:
    """Один случайный k-swap."""
    if sum(y) < k:
        raise ValueError(f"sum(y)={sum(y)} < k={k}")
    one = [i for i in range(len(y)) if y[i] == 1]
    zero = [i for i in range(len(y)) if y[i] == 0]
    v = list(y)
    for i in random.sample(one, k):
        v[i] = 0
    for i in random.sample(zero, k):
        v[i] = 1
    return v


def neighborhood_search(
    y: list[int],
    problem,
    V: float,
    p: int,
    n: int,
    iters: int = 20,
) -> list[int]:
    """Локальный поиск с рандомным 1-swap (итераций: p*(n-p))."""
    vector_opt = y
    local_opt = rc(y, problem, V)
    for _ in range(iters):
        v = random_swap(y)
        r = rc(v, problem, V)
        if r > local_opt:
            local_opt = r
            vector_opt = v
    return vector_opt


def solve(problem, p: int, V: float, seed: int | None = None) -> tuple[float, list[int]]:
    """VND legacy v1: neighborhood_search (1-swap) + escape через K_swap(2).

    :return: (rho, y)
    """
    if seed is not None:
        random.seed(seed)

    n = problem.n
    y_start = generate_y_start(n, p)

    vector_opt = neighborhood_search(y_start, problem, V, p, n)
    local_opt = rc(vector_opt, problem, V)

    for _ in range(20):
        v = neighborhood_search(vector_opt, problem, V, p, n)
        r = rc(v, problem, V)
        if r > local_opt:
            vector_opt = v
            local_opt = r

    for _ in range(100):
        v = k_swap(vector_opt, 2)
        r = rc(v, problem, V)
        if r > local_opt:
            vector_opt = v
            local_opt = r
            break

    return local_opt, vector_opt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VND legacy v1 (random swap + K_swap)")
    parser.add_argument("--data", required=True, help="Путь к файлу данных")
    parser.add_argument("--p", type=int, required=True, help="Количество центров")
    parser.add_argument("--V", type=float, required=True, help="Бюджет")
    parser.add_argument("--seed", type=int, default=None, help="Seed")
    args = parser.parse_args()

    problem = load_dataset(args.data)
    start = time.time()

    rho_val, y_vec = solve(problem, args.p, args.V, seed=args.seed)

    print(f"rho: {rho_val:.4f}")
    print("Solution vector:", y_vec)
    print("Elapsed: {:.2f}s".format(time.time() - start))

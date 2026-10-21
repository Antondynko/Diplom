"""Legacy: VND с рандомным 1-swap + K_swap (2-swap), min cost.

Логика — из VND_algo_2.py. Вводная задача (поиск V), не основная.
Запуск: python -m vnd.heuristic.vnd_legacy_2 --data datasets/30_30_15.txt --p 15
"""

import argparse
import random
import time

from vnd.data import load_dataset
from vnd.model import total_cost
from vnd.neighborhoods import generate_y_start
from vnd.follower import follower


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


def _vc(y: list[int], problem) -> float:
    """Суммарная стоимость по размещению y (VC в исходнике)."""
    return total_cost(follower(y, problem.d), problem.c)


def neighborhood_search(
    y: list[int],
    problem,
    p: int,
    n: int,
    iters: int = 20,
) -> list[int]:
    """Локальный поиск с рандомным 1-swap, min cost."""
    vector_opt = y
    local_opt = _vc(y, problem)
    for _ in range(iters):
        v = random_swap(y)
        c = _vc(v, problem)
        if c < local_opt:
            local_opt = c
            vector_opt = v
    return vector_opt


def solve(problem, p: int, seed: int | None = None) -> tuple[float, list[int]]:
    """VND legacy v2: neighborhood_search (1-swap, min cost) + escape через K_swap(2).

    :return: (V, y)
    """
    if seed is not None:
        random.seed(seed)

    n = problem.n
    y_start = generate_y_start(n, p)

    vector_opt = neighborhood_search(y_start, problem, p, n)
    local_opt = _vc(vector_opt, problem)

    for _ in range(20):
        v = neighborhood_search(vector_opt, problem, p, n)
        c = _vc(v, problem)
        if c < local_opt:
            vector_opt = v
            local_opt = c

    for _ in range(100):
        v = k_swap(vector_opt, 2)
        c = _vc(v, problem)
        if c < local_opt:
            vector_opt = v
            local_opt = c
            break

    return local_opt, vector_opt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VND legacy v2 (random swap, min cost)")
    parser.add_argument("--data", required=True, help="Путь к файлу данных")
    parser.add_argument("--p", type=int, required=True, help="Количество центров")
    parser.add_argument("--seed", type=int, default=None, help="Seed")
    args = parser.parse_args()

    problem = load_dataset(args.data)
    start = time.time()

    V_val, y_vec = solve(problem, args.p, seed=args.seed)

    print(f"V: {V_val:.4f}")
    print("Solution vector:", y_vec)
    print("Elapsed: {:.2f}s".format(time.time() - start))

"""Эвристика VND v1 (актуальная): локальный спуск 1-swap + Improve (2-swap).

Логика и нейминг — из VND_algo_1_NEW.py.
Запуск: python -m vnd.heuristic.vnd_v1 --data datasets/30_30_15.txt --p 15 --V 16000
"""

import argparse
import time

from vnd.data import load_dataset
from vnd.heuristic.common import run_vnd
from vnd.model import rc


def solve(problem, p: int, V: float, seed: int | None = None) -> tuple[float, list[int]]:
    """VND: generate_y_start → local_search ↔ improve.

    :return: (rho, y)
    """
    y = run_vnd(problem, p, V, seed=seed)
    return rc(y, problem, V), y


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VND v1 (актуальная): max rho")
    parser.add_argument("--data", required=True, help="Путь к файлу данных")
    parser.add_argument("--p", type=int, required=True, help="Количество центров")
    parser.add_argument("--V", type=float, required=True, help="Бюджет")
    parser.add_argument("--seed", type=int, default=None, help="Seed для стартового размещения")
    args = parser.parse_args()

    problem = load_dataset(args.data)
    start = time.time()

    rho_val, y_vec = solve(problem, args.p, args.V, seed=args.seed)

    print(f"rho: {rho_val:.4f}")
    print("Solution vector:", y_vec)
    print("Elapsed: {:.2f}s".format(time.time() - start))

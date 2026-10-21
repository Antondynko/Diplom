"""Общий цикл VND: local_search → improve до стабилизации."""

import random

from vnd.data import Problem
from vnd.local_search import improve, local_search
from vnd.model import rc
from vnd.neighborhoods import generate_y_start


def run_vnd(
    problem: Problem,
    p: int,
    V: float,
    seed: int | None = None,
) -> list[int]:
    """Цикл VND: generate_y_start → local_search → improve, пока улучшается.

    :param problem: данные задачи
    :param p: количество центров
    :param V: бюджет
    :param seed: seed для стартового размещения (None = без фиксации)
    :return: итоговое размещение y
    """
    if seed is not None:
        random.seed(seed)

    solve_y = generate_y_start(problem.n, p)

    while True:
        r = local_search(solve_y, problem, V)
        r_rho = rc(r, problem, V)

        s = improve(r, problem, V)
        s_rho = rc(s, problem, V)

        if s_rho > r_rho:
            solve_y = s
            continue
        break

    return s

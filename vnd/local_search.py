"""Локальный поиск и улучшение размещения.

Логика — из VND_algo_1_NEW.py (N, Local_Search, Improve).
"""

from vnd.data import Problem
from vnd.follower import follower
from vnd.model import rho
from vnd.neighborhoods import swap, swap_2


def _rc(y: list[int], problem: Problem, V: float) -> float:
    """Радиус пороговой устойчивости RC(y) для размещения y."""
    return rho(follower(y, problem.d), problem.c, V)


def n_step(y: list[int], problem: Problem, V: float) -> list[int]:
    """Жадный шаг: первый improving swap из окрестности 1-swap.

    :return: улучшение или y, если улучшения нет
    """
    rho_y = _rc(y, problem, V)
    for v in swap(y):
        if _rc(v, problem, V) > rho_y:
            return v
    return y


def local_search(
    y: list[int],
    problem: Problem,
    V: float,
    max_iters: int = 100,
) -> list[int]:
    """Локальный спуск: итерации n_step до локального оптимума.

    :param y: стартовое размещение
    :param problem: данные задачи
    :param V: бюджет
    :param max_iters: ограничитель на число итераций
    :return: локальный оптимум
    """
    for _ in range(max_iters):
        rho_y = _rc(y, problem, V)
        v = n_step(y, problem, V)
        if _rc(v, problem, V) <= rho_y:
            return v
        y = v
    return y


def improve(y: list[int], problem: Problem, V: float) -> list[int]:
    """Просмотр окрестности 2-swap после локального спуска.

    :return: улучшение или y, если улучшения нет
    """
    rho_y = _rc(y, problem, V)
    for v in swap_2(y):
        if _rc(v, problem, V) > rho_y:
            return v
    return y

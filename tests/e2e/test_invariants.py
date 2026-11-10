"""Инварианты результата VND (дополнение к эталонным и метаморфным тестам).

Проверяется: допустимость (y бинарный, ровно p единиц), согласованность
(заявленное ρ = ρ возвращённого y), монотонность (не хуже старта) и критерий
остановки: у самого результата нет улучшающего соседа в окрестностях 1-swap
и 2-swap. Это локальная оптимальность относительно этих окрестностей,
а не глобальная оптимальность.

Соседи перебираются здесь через itertools, независимо от vnd/neighborhoods.py.
"""

from itertools import combinations

import pytest

from e2e_cases import STARTS_20, TINY_P, TINY_V, V_20, problem_20, tiny_problem
from vnd.heuristic.heuristic_vnd import solve
from vnd.model import rc


def _neighbors(y: list[int], k: int):
    """Все размещения, получаемые закрытием k открытых и открытием k закрытых центров."""
    one = [i for i, v in enumerate(y) if v == 1]
    zero = [i for i, v in enumerate(y) if v == 0]
    for closed in combinations(one, k):
        for opened in combinations(zero, k):
            v = list(y)
            for i in closed:
                v[i] = 0
            for i in opened:
                v[i] = 1
            yield v


def _check_result(problem, p: int, V: float, rho_val: float, y: list[int]) -> None:
    assert len(y) == problem.n
    assert set(y) <= {0, 1}
    assert sum(y) == p
    assert rho_val == rc(y, problem, V)
    for k in (1, 2):
        best_neighbor = max(rc(v, problem, V) for v in _neighbors(y, k))
        assert best_neighbor <= rho_val, f"есть улучшающий сосед в {k}-swap"


@pytest.mark.parametrize("y_start", [list(s) for s in combinations(range(7), TINY_P)])
def test_tiny_every_start(run_traced, y_start) -> None:
    """Задача 7×7: все C(7,3) = 35 стартов."""
    y_start = [1 if i in y_start else 0 for i in range(7)]
    problem = tiny_problem()

    rho_val, y, _ = run_traced(problem, TINY_P, TINY_V, y_start)

    _check_result(problem, TINY_P, TINY_V, rho_val, y)
    assert rho_val >= rc(y_start, problem, TINY_V)


@pytest.mark.parametrize("name", list(STARTS_20))
def test_dataset_20_fixed_starts(run_traced, name: str) -> None:
    p, y_start = STARTS_20[name]
    problem = problem_20()

    rho_val, y, _ = run_traced(problem, p, V_20, y_start)

    _check_result(problem, p, V_20, rho_val, y)
    assert rho_val >= rc(y_start, problem, V_20)


@pytest.mark.parametrize("p", [5, 10])
@pytest.mark.parametrize("seed", range(3))
def test_dataset_20_random_starts(p: int, seed: int) -> None:
    """Публичный вход solve(seed=...) без подмен — алгоритм целиком как чёрный ящик."""
    problem = problem_20()

    rho_val, y = solve(problem, p, V_20, seed=seed)

    _check_result(problem, p, V_20, rho_val, y)

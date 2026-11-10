"""Эталонные e2e-тесты VND: фиксированный старт → заранее известный ответ и путь.

При фиксированном старте алгоритм детерминирован (порядок обхода окрестностей
фиксирован, улучшение — строгое, равенства в follower — меньший индекс),
поэтому требуется точное совпадение решения и всего пути поиска.

Ожидаемые значения получены один раз вне тестов независимой реализацией
(свой follower, свои окрестности, сравнение стоимостей) и проверены полным
перебором всех C(n, p) размещений; часть стоимостей пересчитана вручную.
Подробности — docs/testing.md.
"""

import pytest

from e2e_cases import STARTS_20, TINY_P, TINY_STARTS, TINY_V, V_20, problem_20, tiny_problem


class TestTinyProblem:
    """Задача 7×7, p = 3, V = 59. Глобальный минимум стоимости f* = 52 (перебор C(7,3) = 35)."""

    def test_two_swap_fires_then_reaches_global_optimum(self, run_traced) -> None:
        """f: 60 → 56 (1-swap) → 54 (2-swap) → 52 (1-swap), 2-swap больше не срабатывает."""
        rho_val, y, trace = run_traced(tiny_problem(), TINY_P, TINY_V, TINY_STARTS["two_swap_fires"])

        assert y == [1, 1, 0, 0, 0, 0, 1]
        assert rho_val == pytest.approx((59 - 52) / 7)
        assert [c.one_swap for c in trace.cycles] == [
            [[0, 1, 1, 0, 1, 0, 0]],
            [[1, 1, 0, 0, 0, 0, 1]],
        ]
        assert [c.two_swap for c in trace.cycles] == [[1, 0, 0, 0, 1, 0, 1], None]

    def test_descent_without_two_swap(self, run_traced) -> None:
        """f: 59 → 57 → 54 → 52 одним спуском по 1-swap; 2-swap ничего не находит."""
        rho_val, y, trace = run_traced(tiny_problem(), TINY_P, TINY_V, TINY_STARTS["no_two_swap"])

        assert y == [1, 1, 0, 0, 0, 0, 1]
        assert rho_val == pytest.approx((59 - 52) / 7)
        assert [c.one_swap for c in trace.cycles] == [
            [[1, 0, 0, 1, 1, 0, 0], [1, 0, 0, 0, 1, 0, 1], [1, 1, 0, 0, 0, 0, 1]],
        ]
        assert [c.two_swap for c in trace.cycles] == [None]

    def test_stops_at_non_global_local_optimum(self, run_traced) -> None:
        """f: 67 → 63 → 56. f = 56 > f* = 52, но улучшающих соседей в 1-swap и 2-swap нет.

        Это нормальная работа эвристики, а не ошибка.
        """
        rho_val, y, trace = run_traced(tiny_problem(), TINY_P, TINY_V, TINY_STARTS["non_global"])

        assert y == [0, 0, 1, 1, 0, 1, 0]
        assert rho_val == pytest.approx((59 - 56) / 7)
        assert [c.one_swap for c in trace.cycles] == [[[0, 1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 1, 0]]]
        assert [c.two_swap for c in trace.cycles] == [None]


# Глобальные оптимумы на 20_20_15 (перебор C(20,5) = 15 504 и C(20,10) = 184 756 размещений):
#   p = 5:  f* = 9615.992677674925
#   p = 10: f* = 9942.547276716443
Y_P5_GLOBAL = [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0]
RHO_P5_GLOBAL = 19.200366116253736  # (10000 − 9615.992677674925) / 20
Y_P10_GLOBAL = [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0]
RHO_P10_GLOBAL = 2.8726361641778566  # (10000 − 9942.547276716443) / 20
# Неглобальный локальный оптимум при p = 10: f = 9975.308730092336 > f*.
Y_P10_LOCAL = [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1]
RHO_P10_LOCAL = 1.2345634953831905

# имя старта → (ожидаемое y, ожидаемое ρ, [(шагов 1-swap, сработал ли 2-swap), ...])
EXPECTED_20 = {
    "p5_three_cycles": (Y_P5_GLOBAL, RHO_P5_GLOBAL, [(7, True), (2, True), (0, False)]),
    "p10_global": (Y_P10_GLOBAL, RHO_P10_GLOBAL, [(7, True), (0, False)]),
    "p10_no_two_swap": (Y_P10_LOCAL, RHO_P10_LOCAL, [(13, False)]),
    "p10_two_swap_twice": (Y_P10_LOCAL, RHO_P10_LOCAL, [(14, True), (0, True), (1, False)]),
    "p10_one_swap_after_two_swap": (Y_P10_LOCAL, RHO_P10_LOCAL, [(4, True), (2, False)]),
}


@pytest.mark.parametrize("name", list(EXPECTED_20))
def test_dataset_20(run_traced, name: str) -> None:
    """20_20_15, V = 10000: итоговое y, ρ и форма пути поиска."""
    p, y_start = STARTS_20[name]
    expected_y, expected_rho, expected_path = EXPECTED_20[name]

    rho_val, y, trace = run_traced(problem_20(), p, V_20, y_start)

    assert y == expected_y
    assert rho_val == pytest.approx(expected_rho, abs=1e-9)
    assert trace.summary() == expected_path

"""Тесты целевых функций (vnd/model.py)."""

from vnd.data import Problem
from vnd.model import rc, rho, total_cost


class TestTotalCost:
    def test_sums_cost_over_assigned_pairs(self) -> None:
        x = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        c = [[10.0, 20.0, 30.0], [15.0, 25.0, 35.0], [12.0, 22.0, 32.0]]

        assert total_cost(x, c) == 10.0 + 25.0 + 32.0

    def test_zero_when_no_assignment(self) -> None:
        x = [[0.0, 0.0]]
        c = [[10.0, 20.0]]

        assert total_cost(x, c) == 0.0


class TestRho:
    def test_basic(self) -> None:
        x = [[1.0, 0.0]]
        c = [[10.0, 20.0]]

        assert rho(x, c, 100.0) == 45.0

    def test_negative_when_cost_exceeds_budget(self) -> None:
        """Недопустимое размещение даёт отрицательный ρ (градиент для эвристики)."""
        x = [[1.0, 0.0]]
        c = [[150.0, 0.0]]

        assert rho(x, c, 100.0) == -25.0


class TestRc:
    def test_rc_equals_rho_of_follower(self, problem_3x3: Problem) -> None:
        """RC(y) = ρ(follower(y, d), c, V)."""
        from vnd.follower import follower

        y = [1, 0, 0]
        x = follower(y, problem_3x3.d)
        expected = rho(x, problem_3x3.c, 200.0)

        assert rc(y, problem_3x3, 200.0) == expected

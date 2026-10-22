"""Тесты локального поиска (vnd/local_search.py)."""

from vnd.data import Problem
from vnd.local_search import improve, local_search, n_step
from vnd.model import rc
from vnd.neighborhoods import generate_y_start


class TestNStep:
    def test_returns_placement_with_same_size(self, problem_3x3: Problem) -> None:
        y = generate_y_start(3, 2)
        V = 200.0

        result = n_step(y, problem_3x3, V)

        assert len(result) == 3
        assert sum(result) == 2

    def test_does_not_decrease_rho(self, problem_3x3: Problem) -> None:
        y = generate_y_start(3, 2)
        V = 200.0
        rho_before = rc(y, problem_3x3, V)

        result = n_step(y, problem_3x3, V)
        rho_after = rc(result, problem_3x3, V)

        assert rho_after >= rho_before


class TestLocalSearch:
    def test_stops_at_local_optimum(self, problem_3x3: Problem) -> None:
        """После local_search n_step не даёт улучшения."""
        y = generate_y_start(3, 2)
        V = 200.0

        result = local_search(y, problem_3x3, V)
        improved = n_step(result, problem_3x3, V)

        assert rc(improved, problem_3x3, V) <= rc(result, problem_3x3, V)

    def test_respects_max_iters(self, problem_3x3: Problem) -> None:
        y = generate_y_start(3, 2)
        V = 200.0

        result = local_search(y, problem_3x3, V, max_iters=1)

        assert len(result) == 3
        assert sum(result) == 2


class TestImprove:
    def test_does_not_decrease_rho(self, problem_3x3: Problem) -> None:
        y = generate_y_start(3, 2)
        V = 200.0
        rho_before = rc(y, problem_3x3, V)

        result = improve(y, problem_3x3, V)
        rho_after = rc(result, problem_3x3, V)

        assert rho_after >= rho_before

    def test_preserves_placement_size(self, problem_3x3: Problem) -> None:
        y = generate_y_start(3, 2)
        V = 200.0

        result = improve(y, problem_3x3, V)

        assert len(result) == 3
        assert sum(result) == 2

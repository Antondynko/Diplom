"""Метаморфные e2e-тесты VND: известное изменение входа → известное изменение ответа.

Каждое отношение выведено из реализации (порядок обхода окрестностей,
строгое сравнение ρ, разрешение равенств в follower), обоснование —
docs/testing.md. Решение и путь поиска сравниваются точно, ρ — точно, где
арифметика точная (множители 2^k, целые данные), иначе с допуском.

Перестановка центров сюда не входит: она меняет порядок обхода соседей
в swap/swap_2 и разрешение равенств в follower, а значит и путь поиска.
"""

import pytest

from e2e_cases import STARTS_20, TINY_P, TINY_STARTS, TINY_V, V_20, problem_20, tiny_problem
from vnd.data import Problem

CASES = [("tiny", tiny_problem, TINY_P, TINY_V, y) for y in TINY_STARTS.values()] + [
    ("20", problem_20, p, V_20, y) for p, y in STARTS_20.values()
]
IDS = [f"tiny-{name}" for name in TINY_STARTS] + [f"20-{name}" for name in STARTS_20]


def _cycles(trace) -> list[tuple[list[list[int]], list[int] | None]]:
    """Полный путь поиска для точного сравнения."""
    return [(c.one_swap, c.two_swap) for c in trace.cycles]


def _with(problem: Problem, c=None, d=None) -> Problem:
    return Problem(n=problem.n, m=problem.m, c=c or problem.c, d=d or problem.d)


def test_cases_cover_both_phases(run_traced) -> None:
    """Служебная проверка: выбранные старты задействуют и 1-swap, и 2-swap,
    и хотя бы в одном прогоне больше одного цикла VND."""
    summaries = [run_traced(make(), p, V, y)[2].summary() for _, make, p, V, y in CASES]

    assert any(steps > 0 for s in summaries for steps, _ in s)
    assert any(fired for s in summaries for _, fired in s)
    assert any(len(s) > 1 for s in summaries)
    assert any(s == [(s[0][0], False)] for s in summaries)  # 2-swap ни разу не сработал


@pytest.mark.parametrize("kind, make, p, V, y_start", CASES, ids=IDS)
class TestMetamorphic:
    def test_shift_budget(self, run_traced, kind, make, p, V, y_start) -> None:
        """V → V + Δ: решение и путь те же, ρ → ρ + Δ/m."""
        problem = make()
        delta = 1024.0
        rho0, y0, t0 = run_traced(problem, p, V, y_start)
        rho1, y1, t1 = run_traced(problem, p, V + delta, y_start)

        assert y1 == y0
        assert _cycles(t1) == _cycles(t0)
        assert rho1 == pytest.approx(rho0 + delta / problem.m, abs=1e-9)

    def test_scale_cost_and_budget(self, run_traced, kind, make, p, V, y_start) -> None:
        """c → 4c, V → 4V: решение и путь те же, ρ → 4ρ (точно: множитель — степень двойки)."""
        problem = make()
        scaled = _with(problem, c=[[4 * v for v in row] for row in problem.c])
        rho0, y0, t0 = run_traced(problem, p, V, y_start)
        rho1, y1, t1 = run_traced(scaled, p, 4 * V, y_start)

        assert y1 == y0
        assert _cycles(t1) == _cycles(t0)
        assert rho1 == 4 * rho0

    def test_shift_cost_per_client(self, run_traced, kind, make, p, V, y_start) -> None:
        """c[i][j] → c[i][j] + a_j: решение и путь те же, ρ → ρ − Σa_j / m."""
        problem = make()
        a = [j + 1 for j in range(problem.m)]
        shifted = _with(problem, c=[[v + a[j] for j, v in enumerate(row)] for row in problem.c])
        rho0, y0, t0 = run_traced(problem, p, V, y_start)
        rho1, y1, t1 = run_traced(shifted, p, V, y_start)

        assert y1 == y0
        assert _cycles(t1) == _cycles(t0)
        assert rho1 == pytest.approx(rho0 - sum(a) / problem.m, abs=1e-9)

    def test_scale_preferences(self, run_traced, kind, make, p, V, y_start) -> None:
        """d → 4d: назначения follower не меняются, ρ, решение и путь те же (точно)."""
        problem = make()
        scaled = _with(problem, d=[[4 * v for v in row] for row in problem.d])
        rho0, y0, t0 = run_traced(problem, p, V, y_start)
        rho1, y1, t1 = run_traced(scaled, p, V, y_start)

        assert y1 == y0
        assert _cycles(t1) == _cycles(t0)
        assert rho1 == rho0

    def test_shift_preferences_per_client(self, run_traced, kind, make, p, V, y_start) -> None:
        """d[i][j] → d[i][j] + b_j: порядок центров для каждого клиента тот же, всё совпадает точно."""
        problem = make()
        b = [3 * j for j in range(problem.m)]
        shifted = _with(problem, d=[[v + b[j] for j, v in enumerate(row)] for row in problem.d])
        rho0, y0, t0 = run_traced(problem, p, V, y_start)
        rho1, y1, t1 = run_traced(shifted, p, V, y_start)

        assert y1 == y0
        assert _cycles(t1) == _cycles(t0)
        assert rho1 == rho0

    def test_permute_clients(self, run_traced, kind, make, p, V, y_start) -> None:
        """Перестановка клиентов (столбцов c и d): решение и путь те же, ρ — с допуском
        (меняется только порядок суммирования стоимости)."""
        problem = make()
        perm = list(range(problem.m))[::2] + list(range(problem.m))[1::2]
        permuted = _with(
            problem,
            c=[[row[j] for j in perm] for row in problem.c],
            d=[[row[j] for j in perm] for row in problem.d],
        )
        rho0, y0, t0 = run_traced(problem, p, V, y_start)
        rho1, y1, t1 = run_traced(permuted, p, V, y_start)

        assert y1 == y0
        assert _cycles(t1) == _cycles(t0)
        assert rho1 == pytest.approx(rho0, abs=1e-9)

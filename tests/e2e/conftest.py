"""Прогон VND с фиксированным стартом и записью пути поиска.

Продакшен-код не меняется: через monkeypatch подменяется только
generate_y_start (возвращает заданный старт), а n_step, local_search и
improve оборачиваются прозрачными «шпионами», которые лишь записывают
принятые шаги и возвращают результат оригинала без изменений.
"""

from dataclasses import dataclass, field
from typing import Callable

import pytest

import vnd.heuristic.common as common
import vnd.local_search as local_search_module
from vnd.data import Problem
from vnd.heuristic.heuristic_vnd import solve


@dataclass
class Cycle:
    """Один цикл VND: спуск по 1-swap, затем просмотр 2-swap."""

    one_swap: list[list[int]] = field(default_factory=list)  # принятые шаги 1-swap
    two_swap: list[int] | None = None  # принятый шаг 2-swap (None — не сработал)


@dataclass
class Trace:
    cycles: list[Cycle] = field(default_factory=list)

    def summary(self) -> list[tuple[int, bool]]:
        """[(число шагов 1-swap, сработал ли 2-swap), ...] по циклам."""
        return [(len(c.one_swap), c.two_swap is not None) for c in self.cycles]


RunTraced = Callable[[Problem, int, float, list[int]], tuple[float, list[int], Trace]]


@pytest.fixture
def run_traced(monkeypatch: pytest.MonkeyPatch) -> RunTraced:
    """Возвращает функцию (problem, p, V, y_start) -> (rho, y, trace)."""

    orig_n_step = local_search_module.n_step
    orig_local_search = common.local_search
    orig_improve = common.improve

    def run(problem: Problem, p: int, V: float, y_start: list[int]) -> tuple[float, list[int], Trace]:
        trace = Trace()

        def start_stub(n: int, p_: int) -> list[int]:
            assert (n, p_) == (len(y_start), sum(y_start)), "старт не согласован с n, p"
            return list(y_start)

        def n_step_spy(y, problem, V):
            v = orig_n_step(y, problem, V)
            if v != y:
                trace.cycles[-1].one_swap.append(list(v))
            return v

        def local_search_spy(y, problem, V, *args, **kwargs):
            trace.cycles.append(Cycle())
            return orig_local_search(y, problem, V, *args, **kwargs)

        def improve_spy(y, problem, V):
            s = orig_improve(y, problem, V)
            if s != y:
                trace.cycles[-1].two_swap = list(s)
            return s

        with monkeypatch.context() as mp:
            mp.setattr(common, "generate_y_start", start_stub)
            mp.setattr(common, "local_search", local_search_spy)
            mp.setattr(common, "improve", improve_spy)
            mp.setattr(local_search_module, "n_step", n_step_spy)
            rho_val, y = solve(problem, p, V)

        return rho_val, y, trace

    return run

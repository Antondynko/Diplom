"""Процедура RC и вспомогательные функции.

x — матрица назначений клиентов: x[i][j] = 1, если клиент j
назначен на центр i (строго одна 1 в каждом столбце).
c — матрица транспортных расходов (n × m).
V — бюджетное ограничение.
m — число клиентов.
"""

from vnd.follower import follower


def total_cost(x: list[list[float]], c: list[list[float]]) -> float:
    """Суммарные транспортные расходы по назначению x."""
    return sum(c[i][j] for i in range(len(x)) for j in range(len(x[0])) if x[i][j])


def rho(x: list[list[float]], c: list[list[float]], V: float) -> float:
    """Радиус пороговой устойчивости (V - стоимость) / m.

    Возвращает отрицательное значение при превышении бюджета (V < f).
    Ноль при недопустимости ломал бы локальный поиск: алгоритм не смог
    бы различить два недопустимых размещения. Отрицательное значение
    даёт градиент — более близкое к допустимому решение побеждает.
    """
    m = len(x[0])
    return (V - total_cost(x, c)) / m


def rc(y: list[int], problem, V: float) -> float:
    """Радиус пороговой устойчивости RC(y) для размещения y.

    Считает follower → x → rho.
    """
    return rho(follower(y, problem.d), problem.c, V)

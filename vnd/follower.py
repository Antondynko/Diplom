"""Решение задачи нижнего уровня: назначение клиентов на открытые центры.

Каждый клиент назначается на открытый центр с минимальным предпочтением d.
"""


def follower(y: list[int], d: list[list[float]]) -> list[list[int]]:
    """Назначает каждого клиента на открытый центр с минимальным d.

    :param y: вектор размещения (y[i] = 1, если центр i открыт)
    :param d: матрица предпочтений (n строк — центры, m столбцов — клиенты)
    :return: матрица назначений x (n × m), x[i][j] = 1 если клиент j на центре i
    """
    n = len(d)
    m = len(d[0])
    x = [[0] * m for _ in range(n)]

    for j in range(m):
        best_i = 0
        best_d = float("inf")
        for i in range(n):
            if d[i][j] < best_d and y[i] == 1:
                best_i = i
                best_d = d[i][j]
        x[best_i][j] = 1

    return x

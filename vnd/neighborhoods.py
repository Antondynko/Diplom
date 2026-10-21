"""Окрестности размещения y: 1-swap и 2-swap.

Функции возвращают списки новых размещений (окрестность), не одно случайное.
Логика — из VND_algo_1_NEW.py.
"""

import random


def generate_y_start(n: int, p: int) -> list[int]:
    """Случайное размещение: p единиц в n позициях."""
    y = [0] * n
    for i in random.sample(range(n), p):
        y[i] = 1
    return y


def pairs(array: list[int]) -> list[tuple[int, int]]:
    """Все неупорядоченные пары элементов массива."""
    return [(array[i], array[j]) for i in range(len(array)) for j in range(i + 1, len(array))]


def swap(y: list[int]) -> list[list[int]]:
    """Окрестность 1-swap: закрывается один центр, открывается другой.

    :return: список всех размещений из окрестности (p*(n-p) штук)
    """
    one = [i for i in range(len(y)) if y[i] == 1]
    zero = [i for i in range(len(y)) if y[i] == 0]

    result = []
    for i in one:
        for j in zero:
            v = list(y)
            v[i] = 0
            v[j] = 1
            result.append(v)
    return result


def swap_2(y: list[int]) -> list[list[int]]:
    """Окрестность 2-swap: закрываются два центра, открываются два других.

    :return: список всех размещений из окрестности 2-swap
    """
    one = [i for i in range(len(y)) if y[i] == 1]
    zero = [i for i in range(len(y)) if y[i] == 0]

    p1 = pairs(one)
    p0 = pairs(zero)

    result = []
    for i in p1:
        for j in p0:
            v = list(y)
            v[i[0]] = 0
            v[i[1]] = 0
            v[j[0]] = 1
            v[j[1]] = 1
            result.append(v)
    return result

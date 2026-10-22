"""Загрузка и генерация входных данных задачи размещения.

Формат файла: 3 строки заголовка, затем по одной строке на пару
(центр i, клиент j) с полями: ``i j c d`` — индексы, транспортные
расходы, предпочтения клиентов.
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Problem:
    """Входные данные задачи размещения."""

    n: int
    m: int
    c: list[list[float]]
    d: list[list[float]]


def load_dataset(path: Path | str) -> Problem:
    """Читает файл данных и возвращает Problem (n, m, c, d).

    n и m определяются из данных (максимальные индексы), не из заголовка.
    p и V из файла не берутся — задаются аргументами решателя.
    """
    text = Path(path).read_text(encoding="utf-8").splitlines()
    if len(text) < 4:
        raise ValueError(f"Файл {path} слишком короткий: {len(text)} строк")

    rows = []
    for line in text[3:]:
        parts = line.split()
        if not parts:
            continue
        rows.append((int(parts[0]), int(parts[1]), float(parts[2]), float(parts[3])))

    n = max(i for i, *_ in rows) + 1
    m = max(j for _, j, *_ in rows) + 1

    c = [[0.0] * m for _ in range(n)]
    d = [[0.0] * m for _ in range(n)]

    for i, j, c_val, d_val in rows:
        c[i][j] = c_val
        d[i][j] = d_val

    return Problem(n=n, m=m, c=c, d=d)


def _normal_matrix(
    n: int, m: int, low: float, high: float, rng: np.random.Generator
) -> list[list[float]]:
    """Матрица n×m из нормального распределения, обрезанная до [low, high]."""
    mean = (low + high) / 2
    std = (high - low) / 6
    matrix = rng.normal(mean, std, (n, m))
    return np.clip(matrix, low, high).tolist()


def generate_dataset(
    n: int,
    m: int,
    p: int,
    c_low: float,
    c_high: float,
    d_low: float,
    d_high: float,
    path: Path | str,
    seed: int | None = None,
) -> Problem:
    """Генерирует случайные c и d, записывает в файл формата n_m_p.txt.

    :param n: количество центров
    :param m: количество клиентов
    :param p: количество выбранных центров (для имени файла и заголовка)
    :param c_low, c_high: диапазон транспортных расходов
    :param d_low, d_high: диапазон предпочтений клиентов
    :param path: путь к файлу для записи
    :param seed: seed для воспроизводимости (None = без фиксации)
    :return: сгенерированный Problem
    """
    rng = np.random.default_rng(seed)
    c = _normal_matrix(n, m, c_low, c_high, rng)
    d = _normal_matrix(n, m, d_low, d_high, rng)

    lines = [f"n = {n}, m = {m}                 {p}"]
    lines.append("i  j  c  d")
    for i in range(n):
        for j in range(m):
            lines.append(f"{i} {j} {c[i][j]:.4f} {d[i][j]:.4f}")

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

    return Problem(n=n, m=m, c=c, d=d)

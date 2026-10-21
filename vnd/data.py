"""Загрузка входных данных задачи размещения из текстового файла.

Формат файла: 3 строки заголовка, затем по одной строке на пару
(центр i, клиент j) с полями: ``i j c d`` — индексы, транспортные
расходы, предпочтения клиентов.
"""

from dataclasses import dataclass
from pathlib import Path


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

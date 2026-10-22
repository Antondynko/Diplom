# Алгоритмы поиска радиуса пороговой устойчивости двухуровневой задачи размещения с предпочтениями клиентов

Задача размещения (p-медиана) с бюджетным ограничением: минимизация «радиуса неудовлетворённости» ρ при фиксированном числе центров p и бюджете V.

## Постановка задачи

Два уровня принятия решений (leader–follower):

- **Leader** выбирает размещение центров `y` (ровно p из n).
- **Follower** назначает каждого клиента на ближайший открытый центр (min d).

Целевая функция — **радиус пороговой устойчивости**

- `c[i][j]` — транспортные расходы
- `d[i][j]` — предпочтения клиентов
- `V` — бюджет
- `m` — число клиентов

Недопустимые размещения (f > V) дают **отрицательный ρ** — это намеренно: эвристика использует градиент ρ для выбора «менее плохого» соседнего размещения.

### Две задачи

| Задача | Цель | Решение |
|---|---|---|
| **Основная** (max ρ) | Найти y с max ρ при заданном V, p | MIP-решатели + эвристики VND |
| **Вводная** (min cost) | Найти минимальный f при заданном p → получить V | MIP-решатели + эвристика |

Решение вводной задачи (V) подставляется в основную как параметр.

## Быстрый старт

```bash
pip install -r requirements.txt
```

### Решатели (MIP)

```bash
# Основная задача: max ρ
python -m vnd.solvers.gurobi_rho --data datasets/30_30_15.txt --p 15 --V 16000
python -m vnd.solvers.scip_rho   --data datasets/30_30_15.txt --p 15 --V 16000
python -m vnd.solvers.cplex_rho  --data datasets/30_30_15.txt --p 15 --V 16000

# Вводная задача: min cost → V
python -m vnd.solvers.gurobi_v --data datasets/30_30_15.txt --p 15
python -m vnd.solvers.scip_v   --data datasets/30_30_15.txt --p 15
```

### Эвристики (VND)

```bash
# Актуальная: полный обход 1-swap + 2-swap
python -m vnd.heuristic.heuristic_vnd --data datasets/30_30_15.txt --p 15 --V 16000

# Legacy: рандомный 1-swap + K_swap (max ρ)
python -m vnd.heuristic.heuristic_vnd_legacy1 --data datasets/30_30_15.txt --p 15 --V 16000

# Legacy: рандомный 1-swap + K_swap (min cost → V)
python -m vnd.heuristic.heuristic_vnd_legacy2 --data datasets/30_30_15.txt --p 15
```

### Генерация данных

```python
from vnd.data import generate_dataset

generate_dataset(100, 100, 15, 100, 1000, 1, 10, "datasets/100_100_15.txt", seed=42)
```

## Тесты

```bash
python -m pytest tests/ -v
```

## Структура проекта

```
Diplom/
├── datasets/              # входные данные (n_m_p.txt + 333Bi_GapC.txt)
├── vnd/                   # основной пакет
│   ├── data.py            # Problem, load_dataset, generate_dataset
│   ├── model.py           # total_cost, rho, rc
│   ├── follower.py        # follower (назначение клиентов)
│   ├── neighborhoods.py   # generate_y_start, swap, swap_2, pairs
│   ├── local_search.py    # n_step, local_search, improve
│   ├── solvers/           # MIP-решатели
│   │   ├── gurobi_rho.py  # max ρ (Gurobi)
│   │   ├── scip_rho.py    # max ρ (SCIP)
│   │   ├── cplex_rho.py   # max ρ (Cplex)
│   │   ├── gurobi_v.py    # min cost → V (Gurobi)
│   │   └── scip_v.py      # min cost → V (SCIP)
│   └── heuristic/         # эвристики VND
│       ├── common.py      # run_vnd (общий цикл)
│       ├── heuristic_vnd.py         # актуальная (полный обход)
│       ├── heuristic_vnd_legacy1.py # рандомный (max ρ)
│       └── heuristic_vnd_legacy2.py # рандомный (min cost)
├── tests/                 # pytest
├── artifacts/             # исходные скрипты (legacy)
└── requirements.txt       # numpy, gurobipy, ortools
```

## Формат данных

Файл `n_m_p.txt`: 3 строки заголовка, затем `i j c d` (индексы, транспортные расходы, предпочтения). n и m определяются из данных, не из заголовка.

```
n = 30, m = 30                 15
i  j  c  d
──────────────────────────────
0 0 541.7 4.2
0 1 612.3 7.8
...
```

## Переменные модели

| Обозначение | Тип | Описание |
|---|---|---|
| `y[i]` | binary | Центр i открыт (Σy = p) |
| `x[i][j]` | binary | Клиент j назначен на центр i |
| `z[k][i][j]` | binary | Клиент k назначен на i, клиент j на k (связь ρ и x) |
| `ρ` | continuous | Радиус пороговой устойчивости |

## Исходные скрипты

Все 10 исходных `.py`-файлов сохранены в `artifacts/`. Они дублируют функционал `vnd/` и не поддерживаются.

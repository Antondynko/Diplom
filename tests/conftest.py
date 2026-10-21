import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from vnd.data import Problem


@pytest.fixture
def problem_3x3() -> Problem:
    """Маленькая задача: 3 центра, 3 клиента."""
    return Problem(
        n=3,
        m=3,
        c=[
            [10, 20, 30],
            [15, 25, 35],
            [12, 22, 32],
        ],
        d=[
            [1, 5, 3],
            [2, 4, 6],
            [3, 2, 1],
        ],
    )


@pytest.fixture
def problem_file_20() -> Problem:
    """Датасет 20_20_15."""
    from vnd.data import load_dataset

    return load_dataset("datasets/20_20_15.txt")

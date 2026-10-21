"""Тесты загрузчика данных (vnd/data.py)."""

from pathlib import Path

import pytest

from vnd.data import load_dataset


class TestLoadDataset:
    def test_reads_20x20_dataset(self) -> None:
        p = load_dataset("datasets/20_20_15.txt")

        assert p.n == 20
        assert p.m == 20
        assert len(p.c) == 20
        assert len(p.c[0]) == 20
        assert len(p.d) == 20
        assert len(p.d[0]) == 20

    def test_reads_40x100_dataset(self) -> None:
        p = load_dataset("datasets/40_100_5.txt")

        assert p.n == 40
        assert p.m == 100
        assert len(p.c) == 40
        assert len(p.c[0]) == 100

    def test_dimensions_from_data_not_header(self) -> None:
        """Заголовок содержит n, m, p (три числа), но m может перекрываться p."""
        p = load_dataset("datasets/30_30_15.txt")

        assert p.n == 30
        assert p.m == 30

    def test_short_file_raises(self, tmp_path: Path) -> None:
        f = tmp_path / "short.txt"
        f.write_text("line1\nline2\nline3\n", encoding="utf-8")

        with pytest.raises(ValueError, match="слишком короткий"):
            load_dataset(f)

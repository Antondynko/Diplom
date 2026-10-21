from vnd.neighborhoods import generate_y_start, pairs, swap, swap_2


class TestPairs:
    def test_basic(self) -> None:
        assert pairs([1, 2, 3]) == [(1, 2), (1, 3), (2, 3)]

    def test_single(self) -> None:
        assert pairs([1]) == []

    def test_empty(self) -> None:
        assert pairs([]) == []


class TestSwap:
    def test_count(self) -> None:
        y = [1, 1, 0, 0]
        assert len(swap(y)) == 2 * 2

    def test_sum_preserved(self) -> None:
        y = [1, 1, 0, 0, 1]
        for v in swap(y):
            assert sum(v) == 3

    def test_one_flipped(self) -> None:
        y = [1, 0, 1, 0]
        for v in swap(y):
            diffs = sum(1 for i in range(len(y)) if v[i] != y[i])
            assert diffs == 2

    def test_matches_original(self) -> None:
        """Сравнение с исходной Swap (regression)."""

        def swap_old(y: list[int]) -> list[list[int]]:
            indx_1 = [i for i in range(len(y)) if y[i] == 1]
            indx_0 = [i for i in range(len(y)) if y[i] == 0]
            result = []
            for i in indx_1:
                for j in indx_0:
                    v = list(y)
                    v[i] = 0
                    v[j] = 1
                    result.append(v)
            return result

        y = [1, 0, 1, 0, 1, 0]
        assert swap(y) == swap_old(y)


class TestSwap2:
    def test_count(self) -> None:
        y = [1, 1, 0, 0]
        assert len(swap_2(y)) == 1 * 1

    def test_sum_preserved(self) -> None:
        y = [1, 1, 0, 0, 1]
        for v in swap_2(y):
            assert sum(v) == 3

    def test_four_flipped(self) -> None:
        y = [1, 1, 0, 0, 1, 0]
        for v in swap_2(y):
            diffs = sum(1 for i in range(len(y)) if v[i] != y[i])
            assert diffs == 4

    def test_matches_original(self) -> None:
        """Сравнение с исходной Swap_2 (regression)."""

        def pairs_old(array: list[int]) -> list[tuple[int, int]]:
            return [(array[i], array[j]) for i in range(len(array)) for j in range(i + 1, len(array))]

        def swap_2_old(y: list[int]) -> list[list[int]]:
            indx_1 = [i for i in range(len(y)) if y[i] == 1]
            indx_0 = [i for i in range(len(y)) if y[i] == 0]
            p1 = pairs_old(indx_1)
            p0 = pairs_old(indx_0)
            result = []
            for i in p1:
                for j in p0:
                    v = list(y)
                    v[j[0]] = 1
                    v[j[1]] = 1
                    v[i[0]] = 0
                    v[i[1]] = 0
                    result.append(v)
            return result

        y = [1, 1, 0, 0, 1, 0]
        assert swap_2(y) == swap_2_old(y)

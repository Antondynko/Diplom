"""Тесты назначения клиентов на центры (vnd/follower.py)."""

from vnd.follower import follower


class TestFollower:
    def test_single_open_center_assigns_all_clients_to_it(self) -> None:
        d = [[1.0, 5.0, 3.0], [2.0, 4.0, 6.0], [3.0, 2.0, 1.0]]
        y = [1, 0, 0]

        x = follower(y, d)

        assert x == [[1, 1, 1], [0, 0, 0], [0, 0, 0]]

    def test_each_client_goes_to_min_cost_open_center(self) -> None:
        d = [[1.0, 5.0, 3.0], [2.0, 4.0, 6.0], [3.0, 2.0, 1.0]]
        y = [1, 1, 0]

        x = follower(y, d)

        assert x == [[1, 0, 1], [0, 1, 0], [0, 0, 0]]

    def test_closed_center_gets_no_clients(self) -> None:
        d = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
        y = [0, 1, 0]

        x = follower(y, d)

        assert x == [[0, 0, 0], [1, 1, 1], [0, 0, 0]]

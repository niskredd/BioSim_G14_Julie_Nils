import pytest
from biosim.landscape import Lowland


class Test_Tile:

    @pytest.fixture()
    def create_tile(self):
        return Lowland([1, 1])

    def test_feed_animals(self, create_tile):
        for i in range(10):
            create_tile.fauna("Harbivore", 5, 20)

        create_tile.fodder = 19 * 10

        create_tile.feed_animals()
        for ind in create_tile.herb:
            ind.update_status()

        avg_w, avg_phi = 0.0, 0.0
        for ind in create_tile.herb:
            avg_w += ind.w
            avg_phi += ind.phi

        avg_w = avg_w / 20.0
        avg_phi = avg_phi / 20.0

        avg_phi == pytest.approx(0.75)
        avg_w == pytest.approx(21)

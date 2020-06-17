
import pytest
from biosim.island import Island

class Test_Island:

    @pytest.fixture()
    def create_island(self):
        return Island("WWW\nWHW\nWWW")

    def test_create_island(self):
        island = Island("WWWW\nWHLW\nWDWW\nWWWW")
        island = Island("WWWW\nWHLW\nWDWW\nWDWW")

    def test_adding_animals(self, create_island):
        animals = []
        for i in range(20):
            animals.append({'species': 'Herbivore', 'age': 1, 'weight': 10.})

        create_island.adding_animals({'loc': (2, 2), 'pop': animals})

        sum_animals = 0
        for tile_row in create_island.tiles_lits:
            for tile in tile_row:
                sum_animals += tile.herb.__len__()

        assert 20 == sum_animals
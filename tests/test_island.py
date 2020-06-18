
import pytest
from biosim.island import Island, Water, Herbivore


class TestIsland:

    @pytest.fixture()
    def create_island(self):
        return Island("WWW\nWHW\nWWW")

    def test_tiles_list_raises_error_if_not_valid_landscape_type(self):
        with pytest.raises(ValueError):
            Island('WWW\nFDW\nWWW')

    def test_tiles_list(self, create_island):
        island = create_island
        assert island.tiles_lists.__len__() == 3
        assert isinstance(island.tiles_lists[0][0], Water)

    def test_map_test(self, create_island):
        island = create_island
        with pytest.raises(ValueError):
            assert island.map_test("DWWWHWWWW")
            assert island.map_test("WWWDWWWWW")
            assert island.map_test("WWWWWDWWW")

    def test_size_test(self):
        with pytest.raises(ValueError):
            assert Island("WWWWDDDWWW").size_test()

    def test_rgb_for_map(self, create_island):
        island = create_island
        assert island.rgb_for_map('WDHL') == [[(0.0, 0.0, 1.0), (1.0, 1.0, 0.5),
                                              (0.5, 1.0, 0.5), (0.0, 0.6, 0.0)]]

    def test_adding_animals(self, create_island):
        island = create_island
        population = [
            {'loc': (1,1),
             'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 15}]}
        ]
        create_island.adding_animals(population)
        isinstance(create_island.tiles_lists[0][0].herb[0], Herbivore)
        assert create_island.tiles_lists[0][0].herb[0].a == 1
        assert create_island.tiles_lists[0][0].herb[0].w == 15

    def test_tile_update(self, create_island):
        island = create_island







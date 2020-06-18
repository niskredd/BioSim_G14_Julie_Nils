
import pytest
from pytest_mock import *
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
            {'loc': (2, 2),
             'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 15}]}
        ]
        island.adding_animals(population)
        isinstance(island.tiles_lists[1][1].herb[0], Herbivore)
        assert island.tiles_lists[1][1].herb[0].a == 1
        assert island.tiles_lists[1][1].herb[0].w == 15

    def test_tile_update(self, create_island):
        island = create_island
        population = [
            {'loc': (2, 2),
             'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 15}]}
        ]
        island.adding_animals(population)
        island.tile_update()
        assert island.tiles_lists[1][1].herb[0].a == 2
        assert island.tiles_lists[1][1].herb[0].has_moved is False

    def test_tile_neighbours_are_right_types(self, create_island):
        island = create_island
        island_neighbours = island.tile_neighbours((2, 2))
        assert isinstance(island_neighbours[0], Water)
        assert isinstance(island_neighbours[1], Water)
        assert isinstance(island_neighbours[2], Water)
        assert isinstance(island_neighbours[3], Water)

    def test_tile_neighbours_for_corner_tile(self, create_island):
        island = create_island
        island_neighbours = island.tile_neighbours((1, 1))
        assert island_neighbours.__len__() == 2

    def test_migrate_not_when_animal_already_moved(self):
        island = Island('WWWWW\nWLLLW\nWLLLW\nWLLLW\nWWWWW')
        population = [
            {'loc': (3, 3),
             'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 15}]}
        ]
        island.adding_animals(population)
        island.tiles_lists[2][2].herb[0].has_moved = True
        island.migrate(island.tiles_lists[2][2])
        assert island.tiles_lists[2][2].herb.__len__() == 1

    def test_migrate_not_when_surrounded_by_water(self, create_island):
        island = create_island
        population = [
            {'loc': (2, 2),
             'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 15}]}
        ]
        island.adding_animals(population)
        island.migrate(island.tiles_lists[1][1])
        assert island.tiles_lists[1][1].herb.__len__() == 1

    def test_migrate_removes_animals_from_old_tile(self, mocker):
        island = Island('WWWWW\nWLLLW\nWLLLW\nWLLLW\nWWWWW')
        population = [
            {'loc': (3, 3),
             'pop': [{'species': 'Carnivore', 'age': 3, 'weight': 44}]}
        ]
        island.adding_animals(population)
        mocker.patch('random.random', return_value=0)
        island.migrate(island.tiles_lists[2][2])
        assert island.tiles_lists[2][2].carn.__len__() == 0







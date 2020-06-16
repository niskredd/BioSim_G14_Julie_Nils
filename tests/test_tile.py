# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''


import pytest
from biosim.landscape import Lowland, Carnivore, Herbivore


class TestTile:

    @pytest.fixture()
    def create_tile(self):
        return Lowland((1, 1))

    def test_update_num_animals_returns_right_numbers(self, create_tile):
        tile = create_tile
        tile.fauna('Herbivore', 5, 20)
        assert tile.update_num_animals() == (0, 1)

    def test_fauna_appends_herbivore_to_right_lists(self, create_tile):
        tile = create_tile
        initial_num_herbs = tile.herb.__len__()
        tile.fauna('Herbivore', 5, 20)
        num_herbs = tile.herb.__len__()
        assert initial_num_herbs < num_herbs

    def test_fauna_appends_right_amount_of_animals_to_list(self, create_tile):
        tile = create_tile
        initial_num_carns = tile.carn.__len__()
        tile.fauna('Carnivore', 5, 30)
        assert tile.carn.__len__() == initial_num_carns + 1

    def test_fauna_appends_animal_objects_to_lists(self, create_tile):
        tile = create_tile
        tile.fauna('Carnivore', 5, 20)
        tile.fauna('Herbivore', 5, 20)
        isinstance(tile.herb[-1], Herbivore)
        isinstance(tile.carn[-1], Carnivore)

    def test_fauna_does_not_alter_age_and_weight(self, create_tile):
        tile = create_tile
        tile.fauna('Herbivore', 5, 20)
        assert tile.herb[-1].a == 5
        assert tile.herb[-1].w == 20

    def test_birth_creates_new_animals(self, create_tile):
        tile = create_tile
        for i in range(10):
            tile.fauna('Herbivore', 5, 40)
        initial_pop = tile.herb
        for i in range(10):
            tile.birth()
        assert len(tile.herb) >= len(initial_pop)

    def test_birth_cannot_happen_if_only_one_animal(self, create_tile):
        tile = create_tile
        tile.fauna('Herbivore', 5, 20)
        tile.fauna('Carnivore', 5, 20)
        tile.fauna('Carnivore', 5, 20)
        for i in range(100):
            tile.birth()
        assert len(tile.herb) == 1
        assert len(tile.carn) > len(tile.herb)

    def test_birth_depends_on_weight(self, create_tile):
        tile = create_tile
        for i in range(10):
            tile.fauna('Herbivore', 5, 1)
            tile.fauna('Carnivore', 5, 50)

        for i in range(100):
            tile.birth()
        assert tile.herb.__len__() < tile.carn.__len__()

    def test_feed_animals(self, create_tile):
        for i in range(10):
            create_tile.fauna("Herbivore", 5, 20)

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

        assert avg_phi == pytest.approx(0.75)
        assert avg_w == pytest.approx(21)

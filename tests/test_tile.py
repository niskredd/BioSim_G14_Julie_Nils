# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''


import pytest
from biosim.landscape import Lowland


class Test_Tile:

    @pytest.fixture()
    def create_tile(self):
        return Lowland((1, 1))

    def test_birth_creates_new_animals(self, create_tile):
        tile = create_tile
        for i in range(10):
            tile.fauna('Herbivore', 5, 40)
        initial_pop = tile.herb
        tile.birth()
        assert len(tile.herb) >= len(initial_pop)

    def test_birth_cannot_happen_if_only_one_animal(self, create_tile):
        tile = create_tile
        tile.herb = [Animal.Herbivore(5,20)]
        tile.fauna('Carnivore', 5, 20)
        tile.fauna('Carnivore', 5, 20)
        for i in range(100):
            tile.birth()
        assert len(tile.herb) == 1
        assert len(tile.carn) > len(tile.herb)

    def test_birth_depends_on_weight(self, create_tile):
        tile = create_tile
        tile.fauna('Herbivore', 5, 15)
        tile.fauna('Herbivore', 5, 15)
        tile.fauna('Carnivore', 5, 30)
        tile.fauna('Carnivore', 5, 30)
        for i in range(100):
            tile.birth()
        assert len(tile.herb) < len(tile.carn)

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

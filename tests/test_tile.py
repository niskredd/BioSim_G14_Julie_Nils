# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''


import pytest
from biosim.landscape import Tile, Lowland, Highland, Desert, Water, \
    Carnivore, Herbivore


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

    def test_adding_animals_increases_num_animals(self, create_tile):
        animals_to_add = [{'species': 'Herbivore', 'age': 3, 'weight': 43},
                          {'species': 'Carnivore', 'age': 1, 'weight': 28}]
        tile = create_tile
        (num_herbs, num_carns) = (tile.herb.__len__(), tile.carn.__len__())
        tile.adding_animal(animals_to_add)
        assert (
                   tile.herb.__len__(), tile.carn.__len__()) == \
               (num_herbs + 1, num_carns + 1)

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

    def test_death_depends_on_death_prob_and_weight(self, create_tile):
        tile = create_tile
        tile.adding_animal([{'species': 'Herbivore', 'age': 3, 'weight': 0},
                          {'species': 'Carnivore', 'age': 1, 'weight': 0}])
        tile.death()
        assert tile.carn.__len__() + tile.herb.__len__() == 0

    def test_death_removes_herbivores_from_right_list(self, create_tile):
        tile = create_tile
        tile.adding_animal([{'species': 'Herbivore', 'age': 3, 'weight': 0}])
        initial_herbivores = tile.herb.__len__()
        tile.death()
        assert tile.herb.__len__() < initial_herbivores

    def test_death_removes_carnivores_from_right_list(self, create_tile):
        tile = create_tile
        tile.adding_animal([{'species': 'Carnivore', 'age': 3, 'weight': 0}])
        initial_carnivores = tile.carn.__len__()
        tile.death()
        assert tile.carn.__len__() < initial_carnivores

    def test_feed_animals_increases_herb_fitness_and_weight(self, create_tile):
        tile = create_tile
        tile.adding_animal([{'species': 'Herbivore', 'age': 3, 'weight': 10},
                            {'species': 'Herbivore', 'age': 3, 'weight': 10},
                            {'species': 'Herbivore', 'age': 3, 'weight': 10},
                            {'species': 'Herbivore', 'age': 3, 'weight': 10},
                            {'species': 'Herbivore', 'age': 3, 'weight': 10}
                            ])
        sum_w_herb, sum_phi_herb = 0.0, 0.0
        for herb in tile.herb:
            sum_w_herb += herb.w
            sum_phi_herb += herb.phi
        initial_avg_phi_herb = sum_phi_herb/tile.herb.__len__()
        initial_avg_w_herb = sum_w_herb/tile.herb.__len__()

        tile.feed_animals()

        sum_w_herb = 0
        sum_phi_herb = 0
        for herb in tile.herb:
            sum_w_herb += herb.w
            sum_phi_herb += herb.phi
        avg_phi_herb = sum_phi_herb/tile.herb.__len__()
        avg_w_herb = sum_w_herb/tile.herb.__len__()

        assert (avg_phi_herb, avg_w_herb) > \
               (initial_avg_phi_herb, initial_avg_w_herb)

    def test_feed_animals_less_fit_herbs_are_killed_first(self, create_tile):
        tile = create_tile
        tile.adding_animal([{'species': 'Carnivore', 'age': 3, 'weight': 30},
                            {'species': 'Herbivore', 'age': 3, 'weight': 1},
                            {'species': 'Herbivore', 'age': 3, 'weight': 1},
                            {'species': 'Herbivore', 'age': 3, 'weight': 1},
                            {'species': 'Herbivore', 'age': 3, 'weight': 1},
                            {'species': 'Herbivore', 'age': 3, 'weight': 30}
                            ])
        sum_phi_herb = 0
        for herb in tile.herb:
            sum_phi_herb += herb.phi
        initial_avg_phi_herb = sum_phi_herb/tile.herb.__len__()

        tile.feed_animals()

        sum_phi_herb = 0
        for herb in tile.herb:
            sum_phi_herb += herb.phi
        avg_phi_herb = sum_phi_herb/tile.herb.__len__()

        assert avg_phi_herb > initial_avg_phi_herb

    def test_feed_animals_fittest_carnivores_eat_first(self, create_tile):
        tile = create_tile
        tile.adding_animal([{'species': 'Carnivore', 'age': 70, 'weight': 3},
                            {'species': 'Carnivore', 'age': 3, 'weight': 40},
                            {'species': 'Herbivore', 'age': 70, 'weight': 15},
                            ])
        tile.animal_update()
        for _ in range(100):
            tile.feed_animals()

        assert tile.herb.__len__() == 0
        assert tile.carn[1].w > 40
        assert tile.carn[0].w < 3

    def test_animal_update(self, create_tile):
        tile = create_tile
        tile.fauna('Herbivore', 1, 15)
        tile.animal_update()
        assert tile.herb[0].a == 2
        assert tile.herb[0].w < 15
        assert tile.herb[0].has_moved is False

    def test_can_migrate(self, create_tile):
        tile = create_tile
        tile.adding_animal([{'species': 'Carnivore', 'age': 10, 'weight': 40}])
        tile.animal_update()

        migrations = 0
        for _ in range(100):
            tile.can_migrate(tile.carn[0])
            migrations += 1

        assert migrations/100 == pytest.approx(39.9, rel=1e02)

    def test_highland_fodder_and_can_move(self):
        tile = Highland((1,1))
        assert tile.can_move is True
        assert tile.fodder == tile.params['fodder']

    def test_update_fodder_amount(self):
        tile = Tile((1,1))
        assert tile.update_fodder_amount() is None

    def test_highland_update_fodder_amount(self):
        tile = Highland((1,1))
        tile.fodder = 0
        tile.update_fodder_amount()
        assert tile.fodder == tile.params['fodder']

    def test_lowland_fodder_and_can_move(self):
        tile = Lowland((1,1))
        assert tile.can_move is True
        assert tile.fodder == tile.params['fodder']

    def test_lowland_update_fodder_amount(self):
        tile = Lowland((1,1))
        tile.fodder = 0
        tile.update_fodder_amount()
        assert tile.fodder == tile.params['fodder']

    def test_water_fodder_and_can_move(self):
        tile = Water((1,1))
        assert tile.can_move is False
        assert tile.fodder == 0

    def test_water_update_fodder_amount(self):
        tile = Water((1,1))
        tile.fodder = 0
        tile.update_fodder_amount()
        assert tile.fodder == 0

    def test_desert_fodder_and_can_move(self):
        tile = Desert((1,1))
        assert tile.can_move is True
        assert tile.fodder == 0

    def test_desert_update_fodder_amount(self):
        tile = Desert((1,1))
        tile.fodder = 0
        tile.update_fodder_amount()
        assert tile.fodder == 0
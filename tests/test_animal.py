import pytest
from biosim.animal import Animal, Herbivore, Carnivore


class Animal_testing:

    @pytest.fixture()
    def create_carn(self):
        carn = Carnivore(5, 10)
        return carn

    @pytest.fixture()
    def create_herb(self):
        herb = Herbivore(5, 10)
        return herb

    def test_age(self):
        for i in range(3):
            self.create_herb._age_update()
        assert 8 == self.create_herb.a

    def test_wight(self):
        an = Animal(2, 0)
        an._weight_update(5)
        assert an.w == 5

    def test_fitness(self):
        an = Animal(10, 10)
        an.fitness_update()
        assert 1 >= an.phi >= 0

    def test__new_born(self):
        an = Animal(0, 0)
        assert an.w != 0

    def test_carnivores(self):
        assert self.create_carn.parms['ganna'] == 0.8

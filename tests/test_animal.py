import pytest
from biosim.animal import Animal, Herbivore, Carnivore


class Test_Animal:

    @pytest.fixture()
    def create_ani(self):
        anim = Animal(5, 10)
        return anim

    def test_age_update(self):
        for i in range(3):
            self.create_ani.age_update()
        assert 8 == self.create_ani.a

    def test_wight_update(self):
        self.create_ani.weight_update(5)
        assert self.create_ani.w == 5

    def test_fitness(self):
        self.create_ani.fitness_update()
        assert 1 >= self.create_ani.phi >= 0

    def test__new_born(self):
        an = Animal(0, 0)
        assert an.w != 0


class Test_Herbivore:

    @pytest.fixture()
    def create_herb(self):
        herb = Herbivore(5, 10)
        return herb


class Test_Carnivore:

    @pytest.fixture()
    def create_carn(self):
        carn = Carnivore(5, 10)
        return carn

    def test_carnivores(self):
        assert self.create_carn.parms['ganna'] == 0.8

import pytest
from biosim.animal import Animal, Herbivore, Carnivore


class Test_Animal:

    @pytest.fixture()
    def create_ani(self):
        anim = Animal(5, 10)
        return anim

    def test_age_update(self, create_ani):
        for i in range(3):
            create_ani.age_update()
        assert 8 == create_ani.a

    def test_fitness(self, create_ani):
        create_ani.fitness_update()
        assert 1 >= create_ani.phi >= 0

    def test__new_born(self):
        an = Animal(0, 0)
        assert an.w != 0

    def test_death(self, create_ani):



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

    def test_carnivores(self, create_carn):
        assert create_carn.params['gamma'] == 0.8

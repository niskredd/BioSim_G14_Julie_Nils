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


class Test_Herbivore:

    @pytest.fixture()
    def create_herb(self):
        herb = Herbivore(5, 10)
        herb.fitness_update()
        return herb

    def test_fitness(self, create_herb):
        create_herb.fitness_update()
        assert 1 >= create_herb.phi >= 0

    def test__new_born(self):
        an = Herbivore(0, 0)
        assert an.w != 0

    def test_death_prob(self, create_herb):
        sum_d = 0
        for i in range(100):
            if create_herb.death_prob():
                sum_d += 1
        assert sum_d >= 1

    def test_birth_prob(self, create_herb):
        assert create_herb.birth_prob(1) == False
        create_herb.w = 25

        sum_b = 0
        for i in range(100):
            create_herb.w += 1
            if create_herb.birth_prob(2+i):
                sum_b += 1
        assert sum_b > 1

    def test_weight_decrease(self, create_herb):
        weight = create_herb.w
        create_herb.weight_decrease(2)
        assert create_herb.w < weight


class Test_Carnivore:

    @pytest.fixture()
    def create_carn(self):
        carn = Carnivore(5, 10)
        return carn

    def test_carnivores(self, create_carn):
        assert create_carn.params['gamma'] == 0.8
        assert create_carn.params['F'] == 50.0

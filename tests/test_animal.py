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
        assert 10 < sum_d < 35

    def test_birth_prob(self, create_herb):
        assert create_herb.birth_prob(1) == False
        create_herb.w = 25

        sum_b = 0
        for i in range(100):
            create_herb.w += 1
            if create_herb.birth_prob(50):
                sum_b += 1
        assert 10 < sum_b < 100

    def test_yearly_weight_update(self, create_herb):
        weight = create_herb.w
        create_herb.yearly_weight_update()
        assert create_herb.w < weight


class Test_Carnivore:

    @pytest.fixture()
    def create_carn(self):
        carn = Carnivore(5, 20)
        carn.fitness_update()
        return carn

    @pytest.fixture()
    def create_herb(self):
        herb = Herbivore(5, 20)
        herb.fitness_update()
        return herb

    def test_carnivores(self, create_carn):
        assert create_carn.params['gamma'] == 0.8
        assert create_carn.params['F'] == 50.0

    def test_kill_herbivore(self, create_carn, create_herb):
        test_val = 0

        for i in range(100):
            res = create_carn.kill_herbivore(create_herb)
            if res:
                test_val += 1
        assert 0 < test_val < 5


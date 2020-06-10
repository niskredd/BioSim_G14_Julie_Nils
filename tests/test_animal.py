import pytest
from biosim.animal import Animal, Herbivore, Carnivore


class TestAnimal:

    @pytest.fixture()
    def create_ani(self):
        anim = Animal(5, 10)
        return anim

    def test_phi_is_zero_when_w_is_zero(self, create_ani):
        if create_ani.w == 0:
            assert create_ani.phi == 0

    def test_w_new_born_normal_distribution(self):
        w_nb = []
        for i in range(100):
            w_nb.append(Herbivore(0, 0).w)

        w_nb_min = \
            Herbivore.params['w_birth'] - Herbivore.params['sigma_birth']
        w_nb_max = \
            Herbivore.params['w_birth'] + Herbivore.params['sigma_birth']
        assert w_nb_min <= sum(w_nb)/len(w_nb) <= w_nb_max

    def test_age_update(self, create_ani):
        for i in range(3):
            create_ani.age_update()
        assert 8 == create_ani.a

    def test_death_prob_if_w_is_zero(self, create_ani):
        if create_ani.w == 0:
            assert create_ani.death_prob()


class TestHerbivore:

    @pytest.fixture()
    def create_herb(self):
        herb = Herbivore(5, 20)
        herb.fitness_update()
        return herb

    def test_fitness(self, create_herb):
        create_herb.fitness_update()
        assert 1 >= create_herb.phi >= 0

    def test_w_new_born_is_not_zero(self):
        an = Herbivore(0, 0)
        assert an.w != 0

    def test_death_prob(self, create_herb):
        sum_d = 0
        for i in range(100):
            if create_herb.death_prob():
                sum_d += 1
        assert 0 <= sum_d <= 100

    def test_birth_prob(self, create_herb):
        assert create_herb.birth_prob(1) == False
        create_herb.w = 25

        sum_b = 0
        for i in range(100):
            create_herb.w += 1
            if create_herb.birth_prob(50):
                sum_b += 1
        assert 10 < sum_b < 95

    def test_yearly_weight_update_increases_w(self, create_herb):
        weight = create_herb.w
        create_herb.yearly_weight_update()
        assert create_herb.w < weight

    def test_yearly_weight_update_increases_right_amount(self, create_herb):
        weight = create_herb.w
        create_herb.yearly_weight_update()
        assert create_herb.w == weight - weight*create_herb.params['eta']


class TestCarnivore:

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
        assert 0 <= test_val <= 100


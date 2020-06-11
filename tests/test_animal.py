import pytest
from biosim.animal import Animal, Herbivore, Carnivore


class TestAnimal:

    @pytest.fixture()
    def create_ani(self):
        """
        Creates animal objects for testing
        :return: obj Animal
        """
        anim = Animal(5, 10)
        return anim

    def test_phi_is_zero_when_w_is_zero(self, create_ani):
        """
        tests if fitness is zero when weight of animal is zero
        """
        if create_ani.w == 0:
            assert create_ani.phi == 0

    def test_w_new_born_normal_distribution(self):
        """
        Tests if average birth weight is between (w_birth - deviation) and
        (w_birth + deviation)
        :return:
        """
        w_nb = []
        for i in range(100):
            w_nb.append(Herbivore(0, 0).w)

        w_nb_min = \
            Herbivore.params['w_birth'] - Herbivore.params['sigma_birth']
        w_nb_max = \
            Herbivore.params['w_birth'] + Herbivore.params['sigma_birth']
        assert w_nb_min <= sum(w_nb)/len(w_nb) <= w_nb_max

    def test_age_update(self, create_ani):
        """
        Tests if animal age is updated with +1 each time ani_update() is called
        """
        for i in range(3):
            create_ani.age_update()
        assert 8 == create_ani.a

    def test_feed_returns_zero_if_param_zero(self, create_ani):
        assert create_ani.feed(0) == 0

    def test_death_prob_if_w_is_zero(self, create_ani):
        """
        Tests if death_prob returns True if animal weight is zero or less
        """
        if create_ani.w <= 0:
            assert create_ani.death_prob()


class TestHerbivore:

    @pytest.fixture()
    def create_herb(self):
        """
        Creates a herbivore object for further testing
        :return: obj Herbivore
        """
        herb = Herbivore(5, 20)
        herb.fitness_update()
        return herb

    def test_w_new_born_is_not_zero(self):
        """
        tests if weight of newborn herbivore is not zero.
        """
        an = Herbivore(0, 0)
        assert an.w != 0

    def test_a_newborn_is_zero(self):
        """
        tests if age of newborn is zero
        """
        newborn = Herbivore(0, 0)
        assert newborn.a == 0

    def test_fitness_update(self, create_herb):
        """
        tests if herbivore fitness is between 0 and 1.
        """
        create_herb.fitness_update()
        assert 1 >= create_herb.phi >= 0

    def test_fitness_increases_when_weight_increases(self, create_herb):
        phi_unfed = create_herb.phi
        create_herb.weight_increase(80)
        create_herb.fitness_update()
        phi_fed = create_herb.phi
        assert phi_unfed < phi_fed

    def test_fitness_update_gives_right_value(self, create_herb):
        create_herb.params['a_half'] = 40
        create_herb.params['phi_age'] = 0.2
        create_herb.params['phi_weight'] = 0.1
        create_herb.params['w_half'] = 10
        create_herb.fitness_update()
        assert create_herb.phi == pytest.approx(0.7303925)

    def test_yearly_weight_update(self, create_herb):
        weight_1 = create_herb.w
        create_herb.yearly_weight_update()
        weight_2 = create_herb.w
        assert weight_2 < weight_1

    def test_death_prob(self, create_herb):
        sum_d = 0
        for i in range(100):
            if create_herb.death_prob():
                sum_d += 1
        assert 0 <= sum_d <= 100

    def test_birth_prob(self, create_herb):
        assert create_herb.birth_prob(1) is False
        create_herb.w = 25

        sum_b = 0
        for i in range(100):
            create_herb.w += 1
            if create_herb.birth_prob(50):
                sum_b += 1
        assert 10 < sum_b < 95


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

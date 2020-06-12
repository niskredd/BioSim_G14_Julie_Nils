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
        if create_ani.w <= 0:
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

    def test_feed_does_not_alter_w_when_param_zero(self, create_ani):
        w1 = create_ani.w
        create_ani.feed(0)
        w2 = create_ani.w
        assert w1 == w2

    def test_death_prob_if_weight_is_zero(self, create_ani):
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

    def test_params_are_right(self, create_herb):
        assert create_herb.params == {'w_birth': 8.0, 'sigma_birth': 1.5,
                                      'beta': 0.9, 'eta': 0.05, 'a_half': 40.,
                                      'phi_age': 0.2, 'w_half': 10.,
                                      'phi_weight': 0.1, 'mu': 0.25,
                                      'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                                      'omega': 0.4, 'F': 10.}

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

    def test_weight_decrease_birth_returns_right_value(self, create_herb):
        assert \
            create_herb.weight_decrease_birth(8) == 8*create_herb.params['xi']

    def test_weight_decrease_birth_is_positive(self, create_herb):
        assert create_herb.weight_decrease_birth(8) > 0

    def test_birth_prob_when_mothers_weight_too_low(self, create_herb):
        create_herb.w =(
            create_herb.params['zeta']*create_herb.params['w_birth']
            + create_herb.params['sigma_birth']
            - 1
        )
        assert create_herb.birth_prob(100) is False

    def test_birth_prob_is_zero_when_animal_is_alone(self, create_herb):
        assert create_herb.birth_prob(1) is False

    def test_death_prob_given_fitness(self, create_herb):
        create_herb.params['omega'] = 0.4
        create_herb.phi = 0.5
        sum_d = 0
        for i in range(100):
            if create_herb.death_prob():
                sum_d += 1
        assert sum_d/100 == pytest.approx(0.2, rel=1e0)

    def test_death_prob_when_fitness_is_one(self, create_herb):
        create_herb.w = 40
        create_herb.phi = 1
        assert create_herb.death_prob() is False

    def test_feed_when_fodder_more_than_desired_amount(self, create_herb):
        w1 = create_herb.w
        food = create_herb.feed(create_herb.params['F'] + 200)
        w2 = create_herb.w
        assert w1 + create_herb.params['beta']*food == w2
        assert food == create_herb.params['F']

    def test_feed_when_fodder_equals_desired_amount(self, create_herb):
        available_fodder = create_herb.params['F']
        food_eaten = create_herb.feed(available_fodder)
        assert food_eaten == available_fodder

    def test_migrate_prob_is_right(self, create_herb):
        assert \
            create_herb.migrate_prob() == \
            create_herb.phi * create_herb.params['mu']

    def test_migrate_prob_increases_when_phi_increases(self, create_herb):
        create_herb.w = 10
        create_herb.a = 60
        m1 = create_herb.migrate_prob()
        create_herb.w = 50
        create_herb.a = 20
        m2 = create_herb.migrate_prob()
        assert m1 < m2

    def test_update_status_alters_params(self, create_herb):
        w1 = create_herb.w
        a1 = create_herb.a
        phi1 = create_herb.phi
        create_herb.update_status()
        w2 = create_herb.w
        a2 = create_herb.a
        phi2 = create_herb.phi
        assert w1 != w2
        assert a1 != a2
        assert phi1 != phi2

    def test_weight_increase_when_fodder_zero(self, create_herb):
        w1 = create_herb.w
        create_herb.weight_increase(0)
        assert create_herb.w == w1

    def test_weight_increase_when_fodder_not_zero(self, create_herb):
        w1 = create_herb.w
        create_herb.weight_increase(80)
        assert w1 < create_herb.w

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

    def test_carnivores_params(self, create_carn):
        assert create_carn.params == {
            'w_birth': 6., 'sigma_birth': 1., 'beta': 0.75, 'eta': 0.125,
            'a_half': 40., 'phi_age': 0.3, 'w_half': 4., 'phi_weight': 0.4,
            'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5, 'xi': 1.5, 'omega': 0.8,
            'F': 50., 'DeltaPhiMax': 10.
        }

    def test_kill_herbivore_when_herb_phi_high(self, create_carn, create_herb):
        herb = create_herb
        herb.phi = 0.9
        create_carn.phi = 0.1
        assert create_carn.kill_herbivore(herb) is False

    def test_kill_herbivore_when_herb_phi_low(self, create_carn, create_herb):
        herb = create_herb
        herb.phi = 0.1
        create_carn.phi = 0.9
        a = 0
        for i in range(100):
            if create_carn.kill_herbivore(herb):
                a += 1


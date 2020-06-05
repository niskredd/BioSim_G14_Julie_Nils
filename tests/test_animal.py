import pytest
from biosim.animal import Animal


def test_age():
    an = Animal(0, 0)
    for i in range(3):
        an._age_update()
    assert 3 == an.a


def test_wight():
    an = Animal(2, 0)
    an._weight_update(5)
    assert an.w == 5


def test_fitness():
    an = Animal(10, 10)
    an.fitness_update()
    assert 1 >= an.phi >= 0


def test__new_born():
    an = Animal(0, 0)
    assert an.w != 0


class TestAnimal:
    """
    Several tests for the animal class
    """

    @pytest.fixture()
    def create_herb(self):
        """Creates a Herbivore object"""
        herb = Herbivore(5, 10)
        return herb

    @pytest.fixture()
    def create_carn(self):
        """Creates a Carnivore object"""
        carn = Carnivore(5, 10)
        return carn

    def test_positive_fitness(self, create_herb, create_carn):
        """Animal should have positive fitness"""

        assert create_herb.fitness > 0, "Fitness should be positive"
        assert create_carn.fitness > 0, "Fitness should be positive"

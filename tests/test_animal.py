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

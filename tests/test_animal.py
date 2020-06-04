import pytest
from biosim.animal import Animal


def test_age():
    an = Animal(0, 0, 0, 0)
    for i in range(3):
        an._age_update()
    assert 3 == an.a


def test_wight():
    an = Animal(0, 0, 0, 0)
    an._weight_update(5)
    assert an.w == 5


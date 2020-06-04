from numpy import random
import numpy as np
from scipy.stats import norm


class Animal:

    def __init__(self, age, pos, weight, param):
        self.a = age
        self.pos = pos
        self.params = param
        if age == 0:
            self._new_born()
        else:
            self.w = weight
        self.phi = 0

    def _new_born(self):
        self.w = norm.rvs(
            loc=self.params['sigma_birth'], scale=self.params['w_birth'])

    def _age_update(self):
        self.a += 1

    def _weight_update(self, gain):
        self.w += gain

    def fitness_update(self):
        if self.w <= 0:
            self.phi = 0
        else:
            self.phi = (
                    1 / (1 + np.exp((self.a - self.params['a_half']) * self.params['phi_age']))
                    * (1 + np.exp((self.w - self.params['w_half']) * self.params['phi_weight'])))

    def position_update(self):
        pass

    def birth(self, num_animals, param):
        if self.w < self.params['zeta'](self.params['w_birth'] + self.params['sigma_birth']):
            return None
        else:
            prob = min(1, self.params['gamma'] * self.phi * (num_animals - 1))
            if random.rand() < prob:
                new_born = Herbivore(0, self.pos, 0, param)
                self.w = new_born.w * self.params['zeta']

                return new_born
            else:
                return None

    def death(self):
        if self.w == 0:
            return True
        else:
            probability = self.params['omega'] * (1 - self.phi)
            if random.rand() < probability:
                return False
            else:
                return True


class Herbivore(Animal):

    def eat(self, food):
        gain = self.params['beta'] * self.params['F']
        self._weight_update(gain)

    def update_status(self, food):
        self.fitness_update()
        self.eat(food)
        self._age_update()


class Carnivore(Animal):

    def update_status(self, food):
        self.fitness_update()
        self.eat(food)
        self._age_update()

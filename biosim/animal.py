from numpy import random
import numpy as np
from scipy.stats import norm


class Animal:

    params = {'w_birth': 8.,
              'sigma_birth': 1.5,
              'beta': 0.9,
              'eta': 0.05,
              'a_half': 40.,
              'phi_age': 0.2,
              'w_half': 10.,
              'phi_weight': 0.1,
              'mu': 0.25,
              'gamma': 0.2,
              'zeta': 3.5,
              'xi': 1.2,
              'omega': 0.4,
              'F': 10.}

    def __init__(self, age, weight):
        self.a = age
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
                    * 1 / (1 + np.exp(-((self.w - self.params['w_half']) * self.params['phi_weight']))))

    def birth(self, num_animals, param):
        if self.w < self.params['zeta'](self.params['w_birth'] + self.params['sigma_birth']):
            return None
        else:
            prob = min(1, self.params['gamma'] * self.phi * (num_animals - 1))
            if random.rand() < prob:
                new_born = Herbivore(0, 0)
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

    def weight_increase(self, food):
        # food is based on Tile class calculation
        gain = self.params['beta'] * food
        self._weight_update(gain)

    def update_status(self, food):
        self.fitness_update()
        self.weight_increase(food)
        self._age_update()


class Carnivore(Animal):

    def update_status(self, food):
        self.fitness_update()
        self.weight_increase(food)
        self._age_update()

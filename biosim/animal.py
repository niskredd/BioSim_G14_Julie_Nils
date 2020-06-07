import numpy as np
from scipy.stats import norm
from random import random


class Animal:

    params = {'w_birth': 8.0,
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
        self.w_gain = 0

    def _new_born(self):
        self.w = norm.rvs(
            loc=self.params['sigma_birth'], scale=self.params['w_birth'])

    def age_update(self):
        self.a += 1

    def weight_update(self):
        self.w += self.w_gain
        self.w -= self.w * self.params['eta']
        self.w_gain = 0

    def weight_decrease(self, newborn_weight):
        self.w -= newborn_weight * self.params['zeta']

    def birth_prob(self, num_animals):
        if self.w < self.params['zeta']*(self.params['w_birth']
                                         + self.params['sigma_birth']):
            return False
        else:
            prob = min(1, self.params['gamma'] * self.phi * (num_animals - 1))
            if random() < prob:
                return True
            else:
                return False

    def death_prob(self):
        if self.w == 0:
            return True
            print('dead weight')
        else:
            probability = self.params['omega'] * (1 - self.phi)
            if random() < probability:
                return True
                print('dead prob')

    def fitness_update(self):
        if self.w <= 0:
            self.phi = 0
        else:
            self.phi = (
                    1 / (1 + np.exp((self.a - self.params['a_half'])
                                    * self.params['phi_age']))
                    * 1 / (1 + np.exp(-((self.w - self.params['w_half'])
                                        * self.params['phi_weight']))))


class Herbivore(Animal):

    def weight_increase(self, food):
        # food is based on Tile class calculation
        self.w_gain += self.params['beta'] * food

    def update_status(self):
        self.fitness_update()
        self.weight_update()
        self.age_update()


class Carnivore(Animal):

    def __init__(self, age, weight):
        Animal.__init__(self, age, weight)
        self.params.update(
            {'w_birth': 6.,
             'sigma_birth': 1.,
             'beta': 0.75,
             'eta': 0.125,
             'a_half': 40.,
             'phi_age': 0.3,
             'w_half': 4.,
             'phi_weight': 0.4,
             'mu': 0.4,
             'gamma': 0.8,
             'zeta': 3.5,
             'xi': 1.5,
             'omega': 0.8,
             'F': 50.,
             'DeltaPhiMax': 10.})

    def update_status(self):
        self.fitness_update()
        self.weight_update()
        self.age_update()

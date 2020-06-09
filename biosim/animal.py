import numpy as np
from scipy.stats import norm
from random import random


class Animal:
    params = None

    def __init__(self, age, weight):
        self.a = age
        if age == 0:
            self._new_born()
        else:
            self.w = weight
        self.phi = 0

    def _new_born(self):
        self.w = np.random.normal(
            scale=self.params['sigma_birth'], loc=self.params['w_birth'])

    def age_update(self):
        self.a += 1

    def yearly_weight_update(self):
        self.w -= self.w * self.params['eta']

    def weight_decrease_birth(self, newborn_weight):
        self.w -= newborn_weight * self.params['xi']

    def birth_prob(self, num_animals):
        if self.w < self.params['zeta'] * (self.params['w_birth']
                                           + self.params['sigma_birth']):
            return False
        else:
            prob = min(1, self.params['gamma'] * self.phi * (num_animals - 1))
            if random() < prob:
                return True
            else:
                return False

    def death_prob(self):
        if self.w <= 0:
            return True
        else:
            probability = self.params['omega'] * (1 - self.phi)
            if random() < probability:
                return True
                print('dead prob')

    def weight_increase(self):
        pass

    def feed(self, fodder):
        if fodder >= self.params['F']:
            self.weight_increase(self.params['F'])
            return self.params['F']
        elif 0 < fodder < self.params['F']:
            self.weight_increase(fodder)
            return fodder
        else:
            return 0

    def fitness_update(self):
        if self.w <= 0:
            self.phi = 0
        else:
            self.phi = (
                    1 / (1 + np.exp((self.a - self.params['a_half'])
                                    * self.params['phi_age']))
                    * 1 / (1 + np.exp(-((self.w - self.params['w_half'])
                                        * self.params['phi_weight']))))

    def update_status(self):
        self.fitness_update()
        self.yearly_weight_update()
        self.age_update()


class Herbivore(Animal):
    """
    Subclass of Animal class.
    Herbivores eat plants and their fitness therefore depend on the landscape
    that surrounds them.
    """
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

    def weight_increase(self, food):
        """
        Calculates the herbivore's weight increase after grazing for a year.
        :param food: amount of fodder consumed
        :return: weight gain
        """
        self.w += self.params['beta'] * food


class Carnivore(Animal):
    """
    Subclass of Animal class.
    Carnivores eat meat and their fitness therefore depends on the amount of
    herbivores available in their surroundings.
    Weight increase depends on the weight of their prey.
    """
    params = {'w_birth': 6.,
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
              'DeltaPhiMax': 10.}

    def kill_herbivore(self, herbivore):
        """
        Calculates the probability of the carnivore killing a herbivore and
        determines whether the
        """
        if self.phi <= herbivore.phi:
            prob = 0
        elif 0 < self.phi - herbivore.phi < self.params['DeltaPhiMax']:
            prob = (self.phi - herbivore.phi) / self.params['DeltaPhiMax']
        else:
            prob = 1

        if random() < prob:
            return True
        else:
            return False

    def weight_increase(self, w_herb):
        """
        Calculates the carnivore's weight increase after eating prey.
        :param self:
        :param w_herb: weight of killed herbivore
        :return: weight increase
        """
        if w_herb > self.params['F']:
            self.w += self.params['F'] * self.params['beta']
        else:
            self.w += w_herb * self.params['beta']


if __name__ == '__main__':
    for i in range(30):
        herb = Herbivore(0, 0)

        herb.fitness_update()

        print(herb.w)
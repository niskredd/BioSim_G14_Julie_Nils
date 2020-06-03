from scipy.stats import norm
from math import exp
from numpy import random

class Herbivore:
    """
    subclass of animal class

    """

    def __init__(self, params):
        self.params = params
        self.a = 0
        self.w = norm.rvs(
            loc=self.params(sigma_birth),scale=self.params(w_birth)
        )
        self.phi = 0


    def age(self):
        self.a += 1
        return self.a

    def weight(self):
        # depends on feeding
        self.w += F * self.params(beta) # should probably be placed in animal subclass where F will be defined
        self.w -= self.w * self.params(eta)
        return self.w

    def fitness(self):
        if self.w <= 0:
            self.phi = 0
        else:
            self.phi = (
                    1/(1 + exp**(self.a - self.params(a_half)) * self.params(phi_age))
                    * (1 + exp**(self.w - self.params(w_half)) * self.params(phi_weight))
        return self.phi

    def migration(self):
        # cannot enter water, nor feed in desert
        # randomly add or subtract 1 from x or y
        pass

    def procreation(self):
        # excludes newborns
        pass

    def death(self):
        # can be killed by carnivore
        if self.w == 0:
            return True
        else:
            probability = self.params(omega)*(1 - self.phi)
            if random.rand() < probability:
                return False
            else:
                return False
from scipy.stats import norm

class Herbivore():
    """
    subclass of animal class

    """

    def __init__(self):
        pass

    def age(self):
        self.age += 1

    def weight(self):
        # depends on feeding
        birth_weight = norm.rvs(loc=1.5,scale=8.0) # normal distribtion
        pass

    def fitness(self):
        # depends on age and weight
        pass

    def migration(self):
        # cannot enter water, nor feed in desert
        pass

    def procreation(self):
        # excludes newborns
        pass

    def death(self):
        # can be killed by carnivore
        pass


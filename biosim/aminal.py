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


class Animal:

    def __init__(self, age, pos, weight):
        self.age = age
        self.pos = pos
        self.weight = weight

    def _age_update(self):
        self.age = self.age + 1

    def _weight_update(self, gain):
        self.weight = self.weight + gain

    def fitness_update(self):
        pass

    def ret_pos(self):
        return self.pos

    def position_update(self):
        pass


class Herbivore(Animal):

    def __init__(self, age, pos, weight, param):
        super.__init__(age, pos, weight)
        self.params = param

    def eat(self, food):
        gain = params.beta * params.F * food
        self._weight_update(gain)


class Carnivore(Animal):

    def __init__(self):
        super.__init__()

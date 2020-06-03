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


class animal:
    age = 0
    weight = 0
    pos = (0, 0)
    fitness = 0
    params = {}

    def __init__(self, age, pos, weight, param):
        self.age = age
        self.pos = pos
        self.weight = weight
        self.params = param

    def age_update(self):
        self.age = self.age + 1

    def weight_update(self, food):
        pass

    def clac_fitness(self):
        pass

    def ret_pos(self):
        return self.pos

    def change_pos(self):
        pass


class herbivore(animal):

    def __init__(self):
        super.__init__()

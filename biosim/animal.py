class Animal:

    def __init__(self, age, pos, weight, param):
        self.a = age
        self.pos = pos
        self.w = weight
        self.params = param

    def _age_update(self):
        self.a += 1

    def _weight_update(self, gain):
        self.w += gain

    def fitness_update(self):
        pass

    def ret_pos(self):
        return self.pos

    def position_update(self):
        pass


class Herbivore(Animal):

    def eat(self, food):
        gain = self.params('beta') * self.params('F')
        self._weight_update(gain)

    def update_status(self):
        self.fitness_update()
        """
        Birth and death
        update food and weight
        """
        self._age_update()


class Carnivore(Animal):

    def update_status(self):
        self.fitness_update()
        """
        Birth and death
        update food and weight
        """
        self._age_update()

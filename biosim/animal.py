
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
        gain = self.params('beta') * self.params('F') * food
        self._weight_update(gain)

    def update_status(self):
        self.fitness_update()
        """
        Birth and death
        update food and weight
        """
        self._age_update()


class Carnivore(Animal):

    def __init__(self, age, pos, weight):
        super.__init__(age, pos, weight)

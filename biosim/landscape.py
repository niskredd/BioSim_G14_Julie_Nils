# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''


from biosim.animal import *
from random import sample, choice


class Tile:
    params = None

    @classmethod
    def set_parameters(cls, params):
        """Set parameters for class."""
        cls.params.update(params)

    def __init__(self, grid_pos):
        self.grid_pos = grid_pos
        self.herb = []
        self.carn = []
        self.fodder = 0

    def update_num_animals(self):
        return self.carn.__len__(), self.herb.__len__()

    def fauna(self, species, age, weight):
        if species == "Herbivore":
            self.herb.append(Herbivore(age, weight))
        elif species == "Carnivore":
            self.carn.append(Carnivore(age, weight))

    def adding_animal(self, animals):
        """
        Adds animals to a specific tile.
        :param animals: list
        """
        for ind in animals:
            self.fauna(ind['species'], ind['age'], ind['weight'])

    def birth(self):
        """
        Checks all the animals in one tile and determent if they should give birth
        :return: none
        """
        newborn_herbs = []
        for ind in self.herb:
            if ind.birth_prob(self.herb.__len__()):
                new_born = Herbivore(0, 0)
                if ind.weight_decrease_birth(new_born.w) < ind.w:
                    ind.w -= ind.weight_decrease_birth(new_born.w)
                    newborn_herbs.append(new_born)
        self.herb.extend(newborn_herbs)

        newborn_carns = []
        for ind in self.carn:
            if ind.birth_prob(self.carn.__len__()):
                new_born = Carnivore(0, 0)
                if ind.weight_decrease_birth(new_born.w) < ind.w:
                    ind.w -= ind.weight_decrease_birth(new_born.w)
                    newborn_carns.append(new_born)
        self.carn.extend(newborn_carns)

    def death(self):
        """
        Uses death probability to determine whether each animal will die.
        Removes dead animals from the herb and carn lists.
        :return: none
        """
        index = 0
        for ind in self.herb:
            if ind.death_prob():
                self.herb.pop(index)
            index += 1

        index = 0
        for ind in self.carn:
            if ind.death_prob():
                self.carn.pop(index)
            index += 1

    def feed_animals(self):
        herbs = sample(self.herb, self.herb.__len__())
        for herb in herbs:
            self.fodder -= herb.feed(self.fodder)
            herb.fitness_update()

        carns = sorted(self.carn, key=lambda x: x.phi, reverse=True)

        amount_eaten = 0

        for carn in carns:
            herbs = sorted(self.herb, key=lambda x: x.phi)
            for herb in herbs:
                if carn.kill_herbivore(herb):
                    self.herb.remove(herb)
                    amount_eaten += carn.feed(herb.w)
                    carn.fitness_update()
                    if amount_eaten >= carn.params['F']:
                        break

    def animal_update(self): # See comment on update status
        for n in self.herb:
            n.update_status()

        for n in self.carn:
            n.update_status()

    def update_fodder_amount(self):
        pass

    def can_migrate(self, animal):
        animal.fitness_update()
        return random() < animal.phi * animal.params['mu']

    def migrate_direction(self):
        animal_list = []

        for ind in self.herb:
            animal_list.append(ind.migrate_prob())

        for ind in self.carn:
            animal_list.append(ind.migrate_prob())

        move_pop = {'move_from': self.grid_pos, 'animals': animal_list}

        return move_pop

    def move(self):
        self.has_moved = True


class Highland(Tile):

    params = {'fodder': 300}

    def __init__(self, grid_pos):
        Tile.__init__(self, grid_pos)
        self.fodder = self.params['fodder']
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = self.params['fodder']


class Lowland(Tile):

    params = {'fodder': 800}

    def __init__(self, grid_pos):
        Tile.__init__(self, grid_pos)
        self.fodder = self.params['fodder']
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = self.params['fodder']


class Desert(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(self, grid_pos)
        self.fodder = 0
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = 0


class Water(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(self, grid_pos)
        self.fodder = 0
        self.can_move = False

    def update_fodder_amount(self):
        self.fodder = 0


if __name__ == '__main__':
    island = Island("WWWW\nWLHW\nWLDW\nWWWW")

    ani_pop = []
    for imd in range(150):
        ani_pop.append({'species': 'Herbivore', 'age': 1, 'weight': 10.})

    for imd in range(20):
        ani_pop.append({'species': 'Carnivore', 'age': 1, 'weight': 10.})

    island.adding_animals([{'loc': (2, 2), 'pop': ani_pop}])

    year = 0
    for i in range(1000):
        print("Year: " + str(year))
        island.tile_update()
        for tile_row in island.tiles_lists:
            for tile in tile_row:
                if tile.can_move:
                    print("Tile: " + str(tile.grid_pos))
                    print("Carn: " + str(tile.carn.__len__()))
                    print("Herb: " + str(tile.herb.__len__()))
        year += 1

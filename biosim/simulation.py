# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''

from biosim.landscape import Island
from biosim.visual import Visual_Plot


class BioSim:

    def __init__(self, island_map, ini_pop, seed=1, ymax_animals=0, cmax_animals=0, hist_specs=0):
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.Island = Island(island_map)

    def set_animal_parameters(self, species, params):
        pass

    def set_landscape_parameters(self, lscape, params):
        pass

    def add_population(self):
        Island.adding_animals(pop)

    def island_update(self, years):
        for i in range(years):
            self.Island.tile_update()

    def print_res(self):
        for tile in Island.tiles_list:
            print(tile.carn.__len__())
            print(tile.herb.__len__())


if __name__ == "__main__":
    pop = {'loc': (1, 1),
           'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.}]}

    sim = BioSim("L", pop)
    sim.add_population()

    sim.island_update(200)

    sim.print_res()
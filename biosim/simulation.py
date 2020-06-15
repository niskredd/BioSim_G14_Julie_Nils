# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''

from biosim.landscape import Island
from biosim.visual import Visual_Plot
from biosim.animal import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland
import numpy

class BioSim:

    def __init__(self, island_map, ini_pop, seed=1, ymax_animals=0, cmax_animals=0, hist_specs=0):
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.island = Island(island_map)
        # self.tiles_list = self.Island.tiles_lists

        self.add_population(self.ini_pop)

        # for tile in numpy.asarray( self.island.tiles_lists).flatten() :
        #     if tile.herb:
        #         print(len(tile.herb))




        # call the add animals here to add animals to the island

    def set_animal_parameters(self, species, params):
        if species == "Herbivore":
            Herbivore.set_parameters(params)
        elif species == "Carnivore":
            Carnivore.set_parameters(params)

    def set_landscape_parameters(self, lscape, params):
        if lscape == "L":
            Lowland.set_parameters(params)
        elif lscape == "H":
            Highland.set_parameters(params)

    def add_population(self, population):
        self.island.adding_animals(population)

    def island_update(self, years):
        for i in range(years):
            self.island.tile_update()

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
# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''

from biosim.landscape import Island
from biosim.animal import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland
#import matplotlib.pyplot as plt


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

        #self.fig = plt.figure()
        #self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.y_herblist = []
        self.y_carnlist = []
        self.time = 0
        self.island_time = []

        # call the add animals here to add animals to the island

    @staticmethod
    def set_animal_parameters(species, params):
        if species == "Herbivore":
            Herbivore.set_parameters(params)
        elif species == "Carnivore":
            Carnivore.set_parameters(params)

    @staticmethod
    def set_landscape_parameters(lscape, params):
        if lscape == "L":
            Lowland.set_parameters(params)
        elif lscape == "H":
            Highland.set_parameters(params)

    def add_population(self, population):
        self.island.adding_animals(population)

    def island_update(self, years):
        self.time = years
        for i in range(years):
            self.animation_data()
            self.island.tile_update()
            self.island_time.append(i)

    def print_res(self):
        for tile_row in self.island.tiles_lists:
            for tile in tile_row:
                if tile.can_move:
                    print(tile.grid_pos)
                    print(tile.carn.__len__())
                    print(tile.herb.__len__())

    def animation_data(self):
        sum_carn = 0
        sum_herb = 0
        for tile_row in self.island.tiles_lists:
            for tile in tile_row:
                if tile.can_move:
                    sum_carn += tile.carn.__len__()
                    sum_herb += tile.herb.__len__()
        self.y_carnlist.append(sum_carn)
        self.y_herblist.append(sum_herb)


if __name__ == "__main__":
    pop = [{'loc': (2, 2),
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
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
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
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
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
                   {'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.}]}]

    sim = BioSim("WWWWW\nWLDLW\nWLDLW\nWLHHW\nWWWWW", pop)

    sim.island_update(400)

    """
    fig, ax = plt.subplots()
    ax.plot(sim.island_time, sim.y_herblist)
    ax.plot(sim.island_time, sim.y_carnlist)

    ax.set(xlabel='Years', ylabel='Animals', title='')
    ax.grid()

    fig.savefig("test.png")
    plt.show()
    """

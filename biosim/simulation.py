# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''


from .aminal import *


class BioSim:

    def __init__(self, island_map, ini_pop, seed, ymax_animals, cmax_animals, hist_specs):
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs

    def set_animal_parameters(self, species, params):
        pass

    def set_landscape_parameters(self, lscape, params):
        pass


if __name__ == "__main__":
    herb = Herbivore(0, (1, 1), 20, params)

    sim = BioSim()

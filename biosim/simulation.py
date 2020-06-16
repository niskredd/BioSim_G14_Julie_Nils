# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''

import numpy as np
import matplotlib.pyplot as plt
from biosim.landscape import Island
from biosim.animal import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland
from biosim.visual import Visualization
import time


class BioSim:

    def __init__(self, island_map, ini_pop, seed=1, ymax_animals=0, cmax_animals=0, hist_specs=0):
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.island = Island(island_map)
        self.rgb_map = self.island.rgb_for_map(island_map)

        self.add_population(self.ini_pop)
        # call the add animals here to add animals to the island
        self.viual = Visualization()
        self.viual.set_plots_for_first_time(self.rgb_map)

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

    def print_res(self):
        for tile_row in self.island.tiles_lists:
            for tile in tile_row:
                if tile.can_move:
                    print(tile.grid_pos)
                    print(tile.carn.__len__())
                    print(tile.herb.__len__())

    def simulate(self, num_years=10, vis_years=100, img_years=100):
        self.time = num_years
        for i in range(num_years):
            print("--- %s seconds ---" % (time.time() - start_time))
            self.island.tile_update()

            self.viual.update_plot(anim_distribution_dict=self.animals_in_tile(),
                                   total_anim_dict=self.sum_animals())

            self.viual.update_histogram(fit_list=self.fitness_list(), age_list=self.age_list(),
                                        wt_list=self.weight_list())

    def animals_in_tile(self):
        row_num = self.island.tiles_lists.__len__()
        col_num = self.island.tiles_lists[0].__len__()

        herb_mat = np.zeros((row_num, col_num))
        carn_mat = np.zeros((row_num, col_num))

        y = 0
        for tile_row in self.island.tiles_lists:
            x = 0
            for tile in tile_row:
                herb_mat[y][x] = tile.herb.__len__()
                carn_mat[y][x] = tile.carn.__len__()
                x += 1
            y += 1

        return {'Herbivore': herb_mat, 'Carnivore': carn_mat}

    def sum_animals(self):

        herb_total = sum(sum(self.animals_in_tile()['Herbivore']))
        carn_total = sum(sum(self.animals_in_tile()['Carnivore']))
        animal_count_dict = {"Herbivore": herb_total, "Carnivore": carn_total}
        return animal_count_dict

    def fitness_list(self):
        herb_lt = [anim.phi for tile_row in self.island.tiles_lists for
                   tile in tile_row for anim in tile.herb]
        carn_lt = [anim.phi for tile_row in self.island.tiles_lists for
                   tile in tile_row for anim in tile.carn]
        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

    def age_list(self):

        herb_lt = [anim.a for tile_row in self.island.tiles_lists for
                   tile in tile_row for anim in tile.herb]
        carn_lt = [anim.a for tile_row in self.island.tiles_lists for
                   tile in tile_row for anim in tile.carn]
        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

    def weight_list(self):

        herb_lt = [anim.w for tile_row in self.island.tiles_lists for
                   tile in tile_row for anim in tile.herb]
        carn_lt = [anim.w for tile_row in self.island.tiles_lists for
                   tile in tile_row for anim in tile.carn]
        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

if __name__ == "__main__":
    start_time = time.time()
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
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'carnivore', 'age': 1, 'weight': 10.},
                   {'species': 'Carnivore', 'age': 1, 'weight': 10.}]}]
    """
    geogr = "WWWWWWWWWWWWWWWWWWWWW\n" \
            "WWWWWWWWHWWWWLLLLLLLW\n" \
            "WHHHHHLLLLWWLLLLLLLWW\n" \
            "WHHHHHHHHHWWLLLLLLWWW\n" \
            "WHHHHHLLLLLLLLLLLLWWW\n" \
            "WHHHHHLLLDDLLLHLLLWWW\n" \
            "WHHLLLLLDDDLLLHHHHWWW\n" \
            "WWHHHHLLLDDLLLHWWWWWW\n" \
            "WHHHLLLLLDDLLLLLLLWWW\n" \
            "WHHHHLLLLDDLLLLWWWWWW\n" \
            "WWHHHHLLLLLLLLWWWWWWW\n" \
            "WWWHHHHLLLLLLLWWWWWWW\n" \
            "WWWWWWWWWWWWWWWWWWWWW"
            """

    sim = BioSim("WWWW\nWLLW\nWLLW\nWWWW", pop)

    sim.simulate(num_years=400, vis_years=1, img_years=1)

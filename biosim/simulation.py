# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''

import numpy as np
import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.animal import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland
from biosim.visual import Visualization
import time
import os, glob


class BioSim:

    def __init__(self, island_map, ini_pop, seed=1, ymax_animals=0, cmax_animals=0, hist_specs=0,
                 img_base=0, img_fmt='png'):
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.island = Island(island_map)
        self.rgb_map = self.island.rgb_for_map(island_map)

        self.img_base = img_base
        self.img_fmt = img_fmt
        self.add_population(self.ini_pop)
        # call the add animals here to add animals to the island
        self.viual = Visualization()
        self.viual.set_plots_for_first_time(self.rgb_map)
        self.year = 0
        self.num_animals = 0

        self.img_name = 00000
        self.path = "C:\\Users\\Nils\\OneDrive\\Documents\\Programering\\Python\\" \
                    "BioSim_G14_Julie_Nils\\biosim\\testfigroot\\"

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

    @property
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

    @property
    def num_animals_per_species(self):

        herb_total = sum(sum(self.animals_in_tile['Herbivore']))
        carn_total = sum(sum(self.animals_in_tile['Carnivore']))

        self.num_animals = herb_total + carn_total

        return {'Herbivore': herb_total, 'Carnivore': carn_total}

    def fitness_list(self):
        herb_lt = [herb.phi for tile_row in self.island.tiles_lists for
                   tile in tile_row for herb in tile.herb]
        carn_lt = [carn.phi for tile_row in self.island.tiles_lists for
                   tile in tile_row for carn in tile.carn]

        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

    def age_list(self):

        herb_lt = [herb.a for tile_row in self.island.tiles_lists for
                   tile in tile_row for herb in tile.herb]
        carn_lt = [carn.a for tile_row in self.island.tiles_lists for
                   tile in tile_row for carn in tile.carn]
        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

    def weight_list(self):

        herb_lt = [herb.w for tile_row in self.island.tiles_lists for
                   tile in tile_row for herb in tile.herb]
        carn_lt = [carn.w for tile_row in self.island.tiles_lists for
                   tile in tile_row for carn in tile.carn]
        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

    def take_screenshot(self):
        str_n = str(self.img_name)
        str_n = str_n.zfill(5)
        string_ = "_"

        plt.savefig(self.path + string_ + str_n + self.img_fmt)
        self.img_name += 1

    def simulate(self, num_years=10, vis_years=1, img_years=1):
        self.viual.set_step_ln(vis_years)
        self.year += num_years
        for i in range(num_years):
            self.island.tile_update()

            if i % vis_years == 0:
                self.viual.update_plot(anim_distribution_dict=self.animals_in_tile(),
                                       total_anim_dict=self.num_animals_per_species)

                self.viual.update_histogram(fit_list=self.fitness_list(), age_list=self.age_list(),
                                            weight_list=self.weight_list())
            if i % img_years == 0:
                self.take_screenshot()


if __name__ == "__main__":
    start_time = time.time()

    herb_list = []
    for i in range(120):
        herb_list.append({'species': 'Herbivore', 'age': 1, 'weight': 10.})

    carn_list = []
    for i in range(50):
        carn_list.append({'species': 'Carnivore', 'age': 1, 'weight': 10.})

    pop = [{'loc': (2, 2),
           'pop': herb_list}]

    pop2 = [{'loc': (2, 2),
            'pop': carn_list}]

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


    map1 = "WWW\nWLW\nWWW"
    map2 = "WWWW\nWLLW\nWLLW\nWWWW"
    map3 = "WWWWWWWWWWWW\n" \
           "WLLDDLWWLLLW\n" \
           "WLHDLHHLLDDW\n" \
           "WLHHLHWWHLDW\n" \
           "WWWLLHHWLDDW\n" \
           "WWWLWWHHLWLW\n" \
           "WWLLWWHWWWLW\n" \
           "WLLLLDDDHLLW\n" \
           "WLHHLDDDHLLW\n" \
           "WLLLDDDDDLLW\n" \
           "WWWWWWWWWWWW"

    sim = BioSim(map3, pop)
    sim.simulate(num_years=100, vis_years=15, img_years=15)
    sim.add_population(pop2)
    sim.simulate(num_years=400)

    print("--- %s seconds ---" % (time.time() - start_time))
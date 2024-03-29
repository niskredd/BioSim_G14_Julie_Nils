# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''

import os
import time

import matplotlib.pyplot as plt
import numpy as np

from biosim.animal import Herbivore, Carnivore
from biosim.island import Island
from biosim.landscape import Lowland, Highland
from biosim.visual import Visualization


class BioSim:
    """This is documentation for the BioSim class"""

    def __init__(self, island_map, ini_pop, seed=1, ymax_animals=0, cmax_animals=0, hist_specs=0,
                 img_base=0, img_fmt='png'):
        """
        The BioSim class controls the entire simulation and all its attributes.
        :param island_map: string
            A string that contains the layout of the island
        :param ini_pop: dictionary
            Contains the population that starts on the island and the start location.
        :param seed: int
            Contains a random seed, this is not implemented due to time restrains
        :param ymax_animals: int
            Not implemented due to time restrains
        :param cmax_animals: int
            Not implemented due to time restrains
        :param hist_specs: int
            Not implemented due to time restrains
        :param img_base: int
            default store location
        :param img_fmt: string
            The file type that the images are being stored as.
        """
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.island = Island(island_map)

        if img_base == 0:
            self._img_base = os.path.join('.', 'images\\')
        else:
            self._img_base = img_base
        self._img_fmt = img_fmt
        self._img_ctr = 0

        self.add_population(self.ini_pop)

        # call the add animals here to add animals to the island
        self.viual = Visualization()
        self.rgb_map = self.island.rgb_for_map(island_map)
        self.viual.set_plots_for_first_time(self.rgb_map)

        self.year = 0
        self.num_animals = 0

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Adds new parameters to de different animal classes
        :param species: string
        :param params: dictionary
        :return: None
        """
        if species == "Herbivore":
            Herbivore.set_parameters(params)
        elif species == "Carnivore":
            Carnivore.set_parameters(params)

    @staticmethod
    def set_landscape_parameters(lscape, params):
        """
        Changes the parameters of Highland or Lowland tiles
        :param lscape: stirng
        :param params: dictionary
        :return: none
        """
        if lscape == "L":
            Lowland.set_parameters(params)
        elif lscape == "H":
            Highland.set_parameters(params)

    def add_population(self, population):
        """
        Adds the animal populatinon to the correct tile or tiles
        :param population: list of dictionary
        :return: none
        """
        self.island.adding_animals(population)

    @property
    def animals_in_tile(self):
        """
        This method creates a dictionary with two matrix's that contains information on how
        many animals of each species in every tile on the island.
        :return: dictionary
        """
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
        """
        Calculates the total number of animals, and both herbivore and carnivore
        :return: Dictionary
            whit the number of carnivore and herbivore on the island
        """
        herb_total = sum(sum(self.animals_in_tile['Herbivore']))
        carn_total = sum(sum(self.animals_in_tile['Carnivore']))

        self.num_animals = herb_total + carn_total

        return {'Herbivore': herb_total, 'Carnivore': carn_total}

    @property
    def fitness_list(self):
        """
        Mankes a list of all the fitness values on the island
        :return: Dictionary
        """
        herb_lt = [herb.phi for tile_row in self.island.tiles_lists for
                   tile in tile_row for herb in tile.herb]
        carn_lt = [carn.phi for tile_row in self.island.tiles_lists for
                   tile in tile_row for carn in tile.carn]

        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

    @property
    def age_list(self):
        """
        Makes a list of the age of all the animals on the island and saves it in a dictionary
        :return: dictionary
        """
        herb_lt = [herb.a for tile_row in self.island.tiles_lists for
                   tile in tile_row for herb in tile.herb]
        carn_lt = [carn.a for tile_row in self.island.tiles_lists for
                   tile in tile_row for carn in tile.carn]
        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

    @property
    def weight_list(self):
        """
        Makes a list of the weight of all the animalis on the island and saves in a dictionary
        :return: dictionary
        """
        herb_lt = [herb.w for tile_row in self.island.tiles_lists for
                   tile in tile_row for herb in tile.herb]
        carn_lt = [carn.w for tile_row in self.island.tiles_lists for
                   tile in tile_row for carn in tile.carn]
        return {'Herbivore': herb_lt, 'Carnivore': carn_lt}

    def take_screenshot(self):
        """
        Captures a screenshot of the simulation window for logging
        :return: none
        """
        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1

    def simulate(self, num_years=10, vis_years=1, img_years=1):
        """
        Runs the simulation of the island for a given number of years. In addition the user can
        specify the update of the visualisation and the interval the images is being stored.
        :param num_years: int
            How many years the simulation is going to run
        :param vis_years: int
            The rate of update in the visual window
        :param img_years: int
            The rate of images is saved
        :return: none
        """
        self.viual.set_step_ln(vis_years)
        self.year += num_years
        for i in range(num_years):
            self.island.tile_update()

            if i % vis_years == 0:
                self.viual.update_plot(anim_distribution_dict=self.animals_in_tile,
                                       total_anim_dict=self.num_animals_per_species)

                self.viual.update_histogram(fit_list=self.fitness_list, age_list=self.age_list,
                                            weight_list=self.weight_list)
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

    pop = [{'loc': (3, 2),
           'pop': herb_list}]

    pop2 = [{'loc': (3, 2),
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

    sim = BioSim(geogr, pop)
    sim.simulate(num_years=100, vis_years=1, img_years=1)
    sim.add_population(pop2)
    sim.simulate(num_years=400, vis_years=1, img_years=1)

    print("--- %s seconds ---" % (time.time() - start_time))

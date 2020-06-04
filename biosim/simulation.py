# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''

herb_params = {'w_birth': 8.,
               'sigma_birth': 1.5,
               'beta': 0.9,
               'eta': 0.05,
               'a_half': 40.,
               'phi_age': 0.2,
               'w_half': 10.,
               'phi_weight': 0.1,
               'mu': 0.25,
               'gamma': 0.2,
               'zeta': 3.5,
               'xi': 1.2,
               'omega': 0.4,
               'F': 10.}

carn_params = {'w_birth': 6.,
               'sigma_birth': 1.,
               'beta': 0.75,
               'eta': 0.125,
               'a_half': 40.,
               'phi_age': 0.3,
               'w_half': 4.,
               'phi_weight': 0.4,
               'mu': 0.4,
               'gamma': 0.8,
               'zeta': 3.5,
               'xi': 1.5,
               'omega': 0.8,
               'F': 50.,
               'DeltaPhiMax': 10.}


from .animal import Herbivore


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
    herb = Herbivore(0, (1, 1), 20, herb_params)

    herb.update_status()

    sim = BioSim()

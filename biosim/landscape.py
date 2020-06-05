from .animal import *
import time
from numpy import random


class Island:

    def __init__(self, ):
        pass

    """
    Return list of tiles with animals
    """
    def check_map(self):
        pass


class Tile:

    def __init__(self, grid_pos):
        self.grid_pos = grid_pos
        self.herb = []
        self.carn = []
        self.fodder = 300

    def update_num_animals(self):
        return len(self.carn), len(self.herb)

    def update_fodder_amount(self):
        self.fodder = 800  # given lowland

    def fodder_per_herb(self):
        return self.fodder / self.herb.__len__()

    def fauna(self, species, age, weight):
        self.herb.append(Herbivore(age, weight))

    def birth(self, animal):
        if animal.w < animal.params['zeta'](animal.params['w_birth']
                                            + animal.params['sigma_birth']):
            return None
        else:
            prob = min(1, animal.params['gamma'] * animal.phi * (animal.herb.__len__() - 1))
            if random.rand() < prob:
                new_born = Herbivore(0, 0)
                animal.w_gain -= new_born.w * animal.params['zeta']

                return new_born
            else:
                return None

    def death(self):
        for n in self.herb:
            if self.herb[n].w == 0:
                self.herb[n].pop()
            else:
                probability = self.herb[n].params['omega'] * (1 - self.herb[n].phi)
                if random.rand(0, 1) > probability:
                    self.herb[n].pop()

    def animal_eat(self, animal_list): # forslag til forkorting av feed_animals
        for animal in animal_list:
            if self.fodder >= 10:
                animal_list[animal].weight_increase(10)
                self.fodder -= 10
            elif 0 > self.fodder > 10:
                animal_list[animal].weight_increase(self.fodder)
                self.fodder = 0
            else:
                break

    def animal_ageing(self):
        for n in self.herb:
            self.herb[n].age_update()

    def animal_weight(self):
        for n in self.herb:
            self.herb[n].weight_update()


def shuffle_list(a_list, a_len):
    return random.shuffle(a_list, a_len)


if __name__ == '__main__':
    teller = 0
    mini_map = Tile((1, 1))

    mini_map.fauna('Herbivore', 10, 12.5)
    mini_map.fauna('Herbivore', 9, 10.5)

    while teller < 100:
        animals_alive = shuffle_list(mini_map.herb, mini_map.herb.__len__())
        mini_map.feed_animals(animals_alive)

        new = mini_map.birth(mini_map.herb[0])
        if new is not None:
            mini_map.herb.append(new)

        mini_map.animal_ageing()
        mini_map.animal_weight()

        mini_map.death()

        mini_map.fodder = 300

        print(mini_map.update_num_animals())
        print(mini_map.fodder_per_herb())
        for i in mini_map.herb:
            print(mini_map.herb[i].phi)

        time.sleep(1)
        teller += 1

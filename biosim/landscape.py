from biosim.animal import *
import time
from random import sample, random


class Island:

    def __init__(self):
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

    def fauna(self, species, age, weight):
        if species == "Herbivore":
            self.herb.append(Herbivore(age, weight))
        elif species == "Carnivore":
            self.herb.append(Herbivore(age, weight))

    def birth(self, ind):

        if ind.birth_prob(self.herb.__len__()):
            new_born = Herbivore(0, 0)
            ind.weight_decrease(new_born.w)
            self.herb.append(new_born)

    def death(self):
        index = 0
        for n in self.herb:
            if n.w == 0:
                self.herb.pop(index)
                print('dead weight')
            else:
                probability = n.params['omega'] * (1 - n.phi)
                if random() < probability:
                    self.herb.pop(index)
                    print('dead prob')
            index += 1

    def feed_animals(self, animal_list):
        for a in animal_list:
            if self.fodder >= 10:
                a.weight_increase(10)
                self.fodder -= 10
            elif 0 > self.fodder > 10:
                a.weight_increase(self.fodder)
                self.fodder = 0
            else:
                break

    def animal_ageing(self):
        for n in self.herb:
            n.age_update()

    def animal_update(self):
        for n in self.herb:
            n.update_status()


def shuffle_list(a_list, a_len):
    return sample(a_list, a_len)


if __name__ == '__main__':
    teller = 0
    mini_map = Tile((1, 1))

    mini_map.fauna('Herbivore', 10, 12.5)
    mini_map.fauna('Herbivore', 9, 10.5)
    mini_map.fauna('Herbivore', 10, 12.5)
    mini_map.fauna('Herbivore', 9, 10.5)
    mini_map.fauna('Herbivore', 10, 12.5)
    mini_map.fauna('Herbivore', 9, 10.5)

    while teller < 100:

        animals_alive = shuffle_list(mini_map.herb, mini_map.herb.__len__())
        mini_map.feed_animals(animals_alive)

        mini_map.animal_update()

        mini_map.death()

        print(mini_map.update_num_animals())
        print(mini_map.fodder)

        sum_1 = 0
        for animal in mini_map.herb:
            sum_1 += animal.w
            mini_map.birth(animal)
        print(sum_1/mini_map.herb.__len__())

        mini_map.fodder = 300

        time.sleep(1)
        teller += 1

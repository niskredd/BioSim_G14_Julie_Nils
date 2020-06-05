from biosim.animal import *
import time
from random import sample


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

    def fauna(self, species, age, weight):
        self.herb.append(Herbivore(age, weight))

    def birth(self, animal):
        if animal.w < animal.params['zeta']*(animal.params['w_birth']
                                             + animal.params['sigma_birth']):
            return None
        else:
            prob = min(1, animal.params['gamma'] * animal.phi * (self.herb.__len__() - 1))
            if random.rand() < prob:
                new_born = Herbivore(0, 0)
                animal.w_gain -= new_born.w * animal.params['zeta']

                return new_born
            else:
                return None

    def death(self):
        index = 0
        for n in self.herb:
            if n.w == 0:
                self.herb.pop(index)
                print('dead weight')
            else:
                probability = n.params['omega'] * (1 - n.phi)
                if random.random() < probability:
                    self.herb.pop(index)
                    print('dead prob')
            index += 1

    def feed_animals(self, animal_list): # forslag til forkorting av feed_animals
        for animal in animal_list:
            if self.fodder >= 10:
                animal.weight_increase(10)
                self.fodder -= 10
            elif 0 > self.fodder > 10:
                animal.weight_increase(self.fodder)
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

    while teller < 100:
        animals_alive = shuffle_list(mini_map.herb, mini_map.herb.__len__())
        mini_map.feed_animals(animals_alive)

        new = mini_map.birth(mini_map.herb[0])
        if new is not None:
            mini_map.herb.append(new)

        mini_map.animal_update()

        mini_map.death()

        print(mini_map.update_num_animals())
        print(mini_map.fodder)

        sum = 0
        for animal in mini_map.herb:
            sum += animal.w
        print(sum/mini_map.herb.__len__())

        mini_map.fodder = 300

        time.sleep(1)
        teller += 1

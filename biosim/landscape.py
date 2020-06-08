from biosim.animal import *
import time
from random import sample, random


class Island:

    def __init__(self):
        self.map = ""
        self.tiles_list = []

    def create_island(self):
        self.map.split('\n')
        x = 1
        y = 1
        for n in map:
            for l in n:
                if l == "W":
                    self.tiles_list.append(Water((x, y)))
                elif l == "D":
                    self.tiles_list.append(Desert((x, y)))
                elif l == "L":
                    self.tiles_list.append(Lowland((x, y)))
                elif l == "H":
                    self.tiles_list.append(Highland((x, y)))
            x += 1
            y += 1

    def adding_animals(self, tile, animals_to_add):
        for ind in animals_to_add:
            tile.fauna(ind)

    #Runs one year on tile
    def tile_update(self):
        pass


class Tile:

    def __init__(self, grid_pos):
        self.grid_pos = grid_pos
        self.herb = []
        self.carn = []
        self.fodder = 300

    def update_num_animals(self):
        return len(self.carn), len(self.herb)

    def fauna(self, species, age, weight):
        if species == "Herbivore":
            self.herb.append(Herbivore(age, weight))
        elif species == "Carnivore":
            self.herb.append(Herbivore(age, weight))

    def adding_animal(self, **animal):
        if animal['species'] == "Herbivore":
            self.herb.append(Herbivore(animal['age'], animal['weight']))
        elif animal['species'] == "Carnivore":
            self.herb.append(Herbivore(animal['age'], animal['weight']))

    def birth(self):
        for ind in self.herb:
            if ind.birth_prob(self.herb.__len__()):
                new_born = Herbivore(0, 0)
                ind.weight_decrease(new_born.w)
                self.herb.append(new_born)

    def death(self):
        index = 0
        for ind in self.herb:
            if ind.death_prob():
                self.herb.pop(index)
            index += 1

    def feed_animals(self):
        herbs = sample(self.herb, len(self.herb))
        for herb in herbs:



    def prey(self, carnivore):
        """
        Happens after herbivores have eaten.
        :param carnivore: carnivore individual
        :return: weight of prey if there is any, else none
        """
        for herbivore in self.herb:

        for herbivore in self.herb:
            carnivore.kill_herbivore(herbivore)

    def animal_ageing(self):
        for n in self.herb:
            n.age_update()

    def animal_update(self):
        for n in self.herb:
            n.update_status()


class Highland(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(grid_pos)
        self.fodder = 300
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = 300


class Lowland(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(grid_pos)
        self.fodder = 800
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = 800


class Desert(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(grid_pos)
        self.fodder = 0
        self.can_move = True


class Water(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(grid_pos)
        self.fodder = 0
        self.can_move = False


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

        animals_alive = mini_map.shuffle_list(mini_map.herb, mini_map.herb.__len__())
        mini_map.feed_animals(animals_alive)

        mini_map.birth()

        mini_map.animal_update()

        mini_map.death()

        print("Year: " + str(teller))
        print("Number of animals: " + str(mini_map.update_num_animals()))

        sum_1 = 0
        sum_2 = 0
        for animal in mini_map.herb:
            sum_1 += animal.w
            sum_2 += animal.a

        print("Avg weight: " + str(sum_1 / mini_map.herb.__len__()))
        print("Avg age: " + str(sum_2 / mini_map.herb.__len__()))

        mini_map.fodder = 300

        time.sleep(1)
        teller += 1

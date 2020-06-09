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
            tile.adding_animal(ind)

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
            self.carn.append(Carnivore(age, weight))

    def adding_animal(self, **animal):
        if animal['species'] == "Herbivore":
            self.herb.append(Herbivore(animal['age'], animal['weight']))
        elif animal['species'] == "Carnivore":
            self.herb.append(Carnivore(animal['age'], animal['weight']))

    def birth(self):
        herbs = self.herb
        for ind in herbs:
            if ind.birth_prob(herbs.__len__()):
                new_born = Herbivore(0, 0)
                if ind.weight_decrease_birth(new_born.w) < ind.w:
                    ind.weight_decrease_birth(new_born.w)
                    self.herb.append(new_born)

        carns = self.carn
        for ind in carns:
            if ind.birth_prob(carns.__len__()):
                new_born = Carnivore(0, 0)
                if ind.weight_decrease_birth(new_born.w) < ind.w:
                    ind.weight_decrease_birth(new_born.w)
                    self.carn.append(new_born)

    def death(self):
        index = 0
        for ind in self.herb:
            if ind.death_prob():
                self.herb.pop(index)
            index += 1

        index = 0
        for ind in self.carn:
            if ind.death_prob():
                self.carn.pop(index)
            index += 1

    def feed_animals(self):
        herbs = sample(self.herb, self.herb.__len__())
        for herb in herbs:
            self.fodder -= herb.feed(self.fodder)

        for index in range(self.herb.__len__()):
            min_phi = self.herb[0]
            for herb in self.herb[index:]:
                if herb.phi < min_phi.phi:
                    min_phi = herb
            self.herb.remove(min_phi)
            self.herb.insert(index, min_phi)

        carns = self.carn
        for index in range(carns.__len__()):
            max_phi = carns[0]
            for carn in carns[index:]:
                if carn.phi > max_phi.phi:
                    max_phi = carn
            carns.remove(max_phi)
            carns.insert(index, max_phi)

        for carn in carns:
            for herb in self.herb:
                if carn.kill_herbivore(herb):
                    self.herb.remove(herb)
                    if carn.feed(herb.w) > 0:
                        break

    def animal_ageing(self):
        for n in self.herb:
            n.age_update()

    def animal_update(self):
        for n in self.herb:
            n.update_status()

        for n in self.carn:
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
        Tile.__init__(self, grid_pos)
        self.fodder = 800
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = 800


class Desert(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(grid_pos)
        self.fodder = 0
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = 0


class Water(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(grid_pos)
        self.fodder = 0
        self.can_move = False

    def update_fodder_amount(self):
        self.fodder = 0


if __name__ == '__main__':
    teller = 0
    mini_map = Lowland([1, 1])

    for i in range(50):
        mini_map.fauna('Herbivore', 5, 20)

    while teller < 300:
        print("Year: " + str(teller))
        print("Number of animals: " + str(mini_map.update_num_animals()))

        if teller == 500:
            for i in range(20):
                mini_map.fauna('Carnivore', 5, 20)

        mini_map.feed_animals()

        mini_map.birth()

        mini_map.animal_update()

        mini_map.death()

        sum_1 = 0
        sum_2 = 0
        for animal in mini_map.herb:
            sum_1 += animal.w
            sum_2 += animal.a

        sum_3 = 0
        sum_4 = 0
        for animal in mini_map.carn:
            sum_3 += animal.w
            sum_4 += animal.a

        print('\n'+"Herbivore:")
        print("Avg weight: " + str(sum_1 / max(mini_map.herb.__len__(), 1)))
        print("Avg age: " + str(sum_2 / max(mini_map.herb.__len__(), 1)))

        print('\n'+"Carnivore: ")
        print("Avg weight: " + str(sum_3 / max(mini_map.carn.__len__(), 1)))
        print("Avg age: " + str(sum_4 / max(mini_map.carn.__len__(), 1)))
        print('\n')

        mini_map.update_fodder_amount()

        time.sleep(1)
        teller += 1

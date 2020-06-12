# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''


from biosim.animal import *
from random import sample


class Island:

    def __init__(self, map):
        """
        Uses the data from the constructor to create the island, the string is
        converted to a list of tiles
        :return:
                None
        """
        if len(map) > 1:
            maps = map.split("\n")
        self.tiles_lists = [[] * maps[0].__len__() for _ in range(maps.__len__())]
        y = 0
        for line in maps:
            x = 0
            for letter in line:
                if letter == "W":
                    self.tiles_lists[y].append(Water((x + 1, y + 1)))
                elif letter == "D":
                    self.tiles_lists[y].append(Desert((x + 1, y + 1)))
                elif letter == "L":
                    self.tiles_lists[y].append(Lowland((x + 1, y + 1)))
                elif letter == "H":
                    self.tiles_lists[y].append(Highland((x + 1, y + 1)))
                x += 1
            y += 1

    def adding_animals(self, pop):
        """
        Adding animals to each tile on the island,
        all animals, both species
        :param tile: (int, int)
        :param animals_to_add: []
                        list of dictionary's
        :return:
                None
        """
        index_y = 0
        for tiles_in_row in self.tiles_lists:
            index_x = 0
            for tile_e in tiles_in_row:
                pos = pop['location']
                if pos == tile_e.grid_pos:
                    tile_e.adding_animal(pop['population'])
                index_x += 1
            index_y += 1

    def tile_update(self):
        """
        Runs all tiles on the island, one year.
        Updates all values
        :return:
            None
        """
        for tile_row in self.tiles_lists:
            for tile_ in tile_row:
                tile_.feed_animals()
                self.migration()
                tile_.birth()
                tile_.animal_update()
                tile_.death()
                tile_.update_fodder_amount()

    @staticmethod
    def tile_neighbours(self, tile):
        neighbour_west = (tile(0), tile(1) - 1)
        neighbour_east = (tile(0), tile(1) + 1)
        neighbour_north = (tile(0) + 1, tile(1))
        neighbour_south = (tile(0) - 1, tile(1))
        return {
            'north': neighbour_north, 'south': neighbour_south,
            'west': neighbour_west, 'east': neighbour_east
        }

    def migrate(self, **tile):
        for animal in tile['population']:
            if animal.can_migrate():
                animal['location'] = random.choice(self.tile_neighbours(tile['location']))

        for destination in self.tile_neighbours(tile['location']):
            destination.adding_animals(tile['population'])

    def is_list_of_list_empty(self, list_of_list):
        for num in list_of_list:
            if num:
                return True
        return False

    def migration(self):

        for tile_row_m in self.tiles_lists:
            for tile_m in tile_row_m:
                to_move = tile_m.migrate_direction()
                (x, y) = tile_m.grid_pos
                if self.is_list_of_list_empty(to_move['animals']):
                    for ind in to_move['animals']:
                        print(ind['dir'])
                        if self.tiles_lists[y-2][x-1].can_move and ind['dir'] == 'north':
                            if ind['species'] == 'Herbivore':
                                tile_m.herb.remove(ind['ind'])
                                self.tiles_lists[y-2][x-1].herb.append(ind['ind'])
                            if ind['species'] == 'Carnivore':
                                tile_m.carn.remove(ind['ind'])
                                self.tiles_lists[y-2][x-1].carn.append(ind['ind'])
                        if self.tiles_lists[y][x-1].can_move and ind['dir'] == 'south':
                            if ind['species'] == 'Herbivore':
                                tile_m.herb.remove(ind['ind'])
                                self.tiles_lists[y - 2][x - 1].herb.append(ind['ind'])
                            if ind['species'] == 'Carnivore':
                                tile_m.carn.remove(ind['ind'])
                                self.tiles_lists[y - 2][x - 1].carn.append(ind['ind'])
                        if self.tiles_lists[y-1][x].can_move and ind['dir'] == 'east':
                            if ind['species'] == 'Herbivore':
                                tile_m.herb.remove(ind['ind'])
                                self.tiles_lists[y - 2][x - 1].herb.append(ind['ind'])
                            if ind['species'] == 'Carnivore':
                                tile_m.carn.remove(ind['ind'])
                                self.tiles_lists[y - 2][x - 1].carn.append(ind['ind'])
                        if self.tiles_lists[y-1][x-2].can_move and ind['dir'] == 'west':
                            if ind['species'] == 'Herbivore':
                                tile_m.herb.remove(ind['ind'])
                                self.tiles_lists[y - 2][x - 1].herb.append(ind['ind'])
                            if ind['species'] == 'Carnivore':
                                tile_m.carn.remove(ind['ind'])
                                self.tiles_lists[y - 2][x - 1].carn.append(ind['ind'])


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

    def adding_animal(self, animal_dir):
        """
        Adds animals to this tiles
        :param animal_dir: {:}
                      directory
        """
        for ind in animal_dir:
            if ind['species'] == 'Herbivore':
                self.herb.append(Herbivore(ind['age'], ind['weight']))
            elif ind['species'] == 'Carnivore':
                self.carn.append(Carnivore(ind['age'], ind['weight']))

    def birth(self):
        herbs = []
        for ind in self.herb:
            if ind.birth_prob(self.herb.__len__()):
                new_born = Herbivore(0, 0)
                if ind.weight_decrease_birth(new_born.w) < ind.w:
                    ind.w -= ind.weight_decrease_birth(new_born.w)
                    herbs.append(new_born)
        self.herb.extend(herbs)

        carns = []
        for ind in self.carn:
            if ind.birth_prob(self.carn.__len__()):
                new_born = Carnivore(0, 0)
                if ind.weight_decrease_birth(new_born.w) < ind.w:
                    ind.w -= ind.weight_decrease_birth(new_born.w)
                    carns.append(new_born)
        self.carn.extend(carns)

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
            herb.fitness_update()

        for index in range(self.herb.__len__()):
            min_phi = self.herb[0]
            for herb in self.herb[index:]:
                if herb.phi < min_phi.phi:
                    min_phi = herb
            self.herb.remove(min_phi)
            self.herb.insert(index, min_phi)

        # herbs = sorted(herbs, key=fitness_key)
        carns = self.carn

        for index in range(carns.__len__()):
            max_phi = carns[0]
            for carn in carns[index:]:
                if carn.phi > max_phi.phi:
                    max_phi = carn
            carns.remove(max_phi)
            carns.insert(index, max_phi)

        # carns = sorted(carns, key=fitness_key, reverse=True)

        for carn in carns:
            for herb in self.herb:
                if carn.kill_herbivore(herb):
                    self.herb.remove(herb)
                    carn.fitness_update()
                    if carn.feed(herb.w) > 0:
                        break

    def animal_ageing(self):
        for n in self.herb:
            n.age_update()

    def animal_update(self): # See comment on update status
        for n in self.herb:
            n.update_status()

        for n in self.carn:
            n.update_status()

    def update_fodder_amount(self):
        pass

    def can_migrate(self, animal):
        animal.fitness_update()
        return random() < animal.phi * animal.params['mu']

    def migrate_direction(self):
        animal_list = []

        for ind in self.herb:
            animal_list.append(ind.migrate_prob())

        for ind in self.carn:
            animal_list.append(ind.migrate_prob())

        move_pop = {'move_from': self.grid_pos, 'animals': animal_list}

        return move_pop


class Highland(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(self, grid_pos)
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
        Tile.__init__(self, grid_pos)
        self.fodder = 0
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = 0


class Water(Tile):

    def __init__(self, grid_pos):
        Tile.__init__(self, grid_pos)
        self.fodder = 0
        self.can_move = False

    def update_fodder_amount(self):
        self.fodder = 0


if __name__ == '__main__':
    island = Island("WWWW\nWLHW\nWLDW\nWWWW")

    ani_pop = []
    for imd in range(150):
        ani_pop.append({'species': 'Herbivore', 'age': 1, 'weight': 10.})

    for imd in range(20):
        ani_pop.append({'species': 'Carnivore', 'age': 1, 'weight': 10.})

    island.adding_animals({'loc': (2, 2), 'pop': ani_pop})

    year = 0
    for i in range(100):
        print("Year: " + str(year))
        island.tile_update()
        for tile_row in island.tiles_lists:
            for tile in tile_row:
                if tile.can_move:
                    print("Tile: " + str(tile.grid_pos))
                    print("Carn: " + str(tile.carn.__len__()))
                    print("Herb: " + str(tile.herb.__len__()))
        year += 1

"""
if __name__ == '__main__':
    teller = 0
    mini_map = Lowland([1, 1])

    for i in range(50):
        mini_map.fauna('Herbivore', 5, 20)

    while teller < 300:
        print("Year: " + str(teller))
        print("Number of animals: " + str(mini_map.update_num_animals()))

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

        sum_5 = 0
        sum_6 = 0
        for animal in mini_map.herb:
            sum_5 += animal.phi

        for animal in mini_map.carn:
            sum_6 += animal.phi

        print('\n' + "Herbivore:")
        print("Avg weight: " + str(sum_1 / max(mini_map.herb.__len__(), 1)))
        print("Avg age: " + str(sum_2 / max(mini_map.herb.__len__(), 1)))
        print("Avg Fitness: " + str(sum_5 / max(mini_map.herb.__len__(), 1)))

        print('\n' + "Carnivore: ")
        print("Avg weight: " + str(sum_3 / max(mini_map.carn.__len__(), 1)))
        print("Avg age: " + str(sum_4 / max(mini_map.carn.__len__(), 1)))
        print("Avg Fitness: " + str(sum_6 / max(mini_map.carn.__len__(), 1)))
        print('\n')

        if teller == 50:
            for i in range(20):
                mini_map.fauna('Carnivore', 5, 20)

        mini_map.feed_animals()

        mini_map.birth()

        mini_map.animal_update()

        mini_map.death()

        mini_map.update_fodder_amount()

        time.sleep(1)
        teller += 1
        """

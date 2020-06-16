# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''


from biosim.animal import *
from random import sample, choice


class Island:

    def __init__(self, map):
        """
        Uses the data from the constructor to create the island, the string is
        converted to a list of tiles
        :return:
                None
        """
        self.map_test(map)

        self.tiles_lists = [
            [] * map.split("\n").__len__() for
            _ in range(map.split("\n").__len__())]

        y = 0
        for line in map.split("\n"):
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
                else:
                    raise ValueError
                x += 1
            y += 1

        self.size_test()

    def map_test(self, map):
        """
        Checks if the map has a water boarder all the way around
        :param map: string
        :return: none
        """
        lines = map.split("\n")
        for letter in lines[0]:
            if not letter == 'W':
                raise ValueError

        for letter in lines[len(lines) - 1]:
            if not letter == 'W':
                raise ValueError

        for line in lines:
            if not line[0] == 'W' or not line[len(line) - 1] == 'W':
                raise ValueError

    def size_test(self):
        """
        tests if the lines on the map is the same lenght
        :return: None
        """
        tiles = iter(self.tiles_lists)
        length_row = next(tiles).__len__()
        if not all(len(tile) == length_row for tile in tiles):
            raise ValueError

    def adding_animals(self, population):
        """
        Adding animals to each tile on the island,
        all animals, both species.

        :param population: list
                            containing both the tile location (loc) and its
                            respective population (pop).
        :return: None
        """

        if population.__len__() == 1:
            (x, y) = population[0]['loc']
            self.tiles_lists[x-1][y-1].adding_animal(population[0]['pop'])
        elif population.__len__() > 1:
            for one_location_dict in population:
                (x, y) = one_location_dict['loc']
                self.tiles_lists[x-1][y-1].adding_animal(one_location_dict['pop'])

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
                self.migrate(tile_)
                tile_.birth()
                tile_.animal_update()
                tile_.death()
                tile_.update_fodder_amount()

    def tile_neighbours(self, position):
        """
        Takes tile position as coordinate and returns its neighbour coordinates
        in a dictionary with key=orientation and val=coordinate.

        :param position: tuple
                        tile coordinate (x, y)
        :return: dict
                    {'neighbour orientation': (x, y), ...}
                    where neighbour orientation can be North, South, West, East
        """
        neighbour_west = (position[0], position[1]-1)
        neighbour_east = (position[0], position[1]+1)
        neighbour_north = (position[0]+1, position[1])
        neighbour_south = (position[0]-1, position[1])
        neighbour_coordinates = [
            neighbour_north, neighbour_south, neighbour_west, neighbour_east
        ]
        neighbours = []
        for neighbour in neighbour_coordinates:
            for tile_row in self.tiles_lists:
                for tile in tile_row:
                    if tile.grid_pos == neighbour:
                        neighbours.append(tile)
        return neighbours

    def migrate(self, tile):
        """

        :param tile: dict
                        dictionary representing a tile with its respective
                        population.
        :return: None
        """
        initial_pop = self.tiles_lists
        if len(tile.herb) > 0:
            for herb in tile.herb:
                if tile.can_migrate(herb):
                    destination = choice(self.tile_neighbours(tile.grid_pos))
                    if not herb.has_moved:
                        if destination.can_move:
                            for tiles_row in initial_pop:
                                for initial_tile in tiles_row:
                                    if initial_tile == destination:
                                        initial_tile.herb.append(herb)
                                        herb.has_moved = True
        if len(tile.carn) > 0:
            for carn in tile.carn:
                if tile.can_migrate(carn):
                    destination = choice(self.tile_neighbours(tile.grid_pos))
                    if not carn.has_moved:
                        if destination.can_move:
                            for tiles_row in initial_pop:
                                for initial_tile in tiles_row:
                                    if initial_tile == destination:
                                        initial_tile.carn.append(carn)
                                        carn.has_moved = True


class Tile:
    params = None

    @classmethod
    def set_parameters(cls, params):
        """Set parameters for class."""
        cls.params.update(params)

    def __init__(self, grid_pos):
        self.grid_pos = grid_pos
        self.herb = []
        self.carn = []
        self.fodder = 300

    def update_num_animals(self):
        return self.carn.__len__(), self.herb.__len__()

    def fauna(self, species, age, weight):
        if species == "Herbivore":
            self.herb.append(Herbivore(age, weight))
        elif species == "Carnivore":
            self.carn.append(Carnivore(age, weight))

    def adding_animal(self, animals):
        """
        Adds animals to a specific tile.
        :param animals: dict
        """
        for ind in animals:
            if ind['species'] == 'Herbivore':
                self.herb.append(Herbivore(ind['age'], ind['weight']))
            elif ind['species'] == 'Carnivore':
                self.carn.append(Carnivore(ind['age'], ind['weight']))

    def birth(self):
        """
        Checks all the animals in one tile and determent if they should give birth
        :return: none
        """
        newborn_herbs = []
        for ind in self.herb:
            if ind.birth_prob(self.herb.__len__()):
                new_born = Herbivore(0, 0)
                if ind.weight_decrease_birth(new_born.w) < ind.w:
                    ind.w -= ind.weight_decrease_birth(new_born.w)
                    newborn_herbs.append(new_born)
        self.herb.extend(newborn_herbs)

        newborn_carns = []
        for ind in self.carn:
            if ind.birth_prob(self.carn.__len__()):
                new_born = Carnivore(0, 0)
                if ind.weight_decrease_birth(new_born.w) < ind.w:
                    ind.w -= ind.weight_decrease_birth(new_born.w)
                    newborn_carns.append(new_born)
        self.carn.extend(newborn_carns)

    def death(self):
        """
        Checks the probability that a animal should live or die
        :return: none
        """
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

        #carns = sorted(carns, key=(carn.phi for carn in carns), reverse=True)

        for carn in carns:
            for herb in self.herb:
                if carn.kill_herbivore(herb):
                    self.herb.remove(herb)
                    carn.fitness_update()
                    if carn.feed(herb.w) > 0:
                        break

    def animal_ageing(self):
        """
        Adds one year to all animals
        :return: none
        """
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

    def move(self):
        self.has_moved = True


class Highland(Tile):

    params = {'fodder': 300}

    def __init__(self, grid_pos):
        Tile.__init__(self, grid_pos)
        self.fodder = self.params['fodder']
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = self.params['fodder']


class Lowland(Tile):

    params = {'fodder': 800}

    def __init__(self, grid_pos):
        Tile.__init__(self, grid_pos)
        self.fodder = self.params['fodder']
        self.can_move = True

    def update_fodder_amount(self):
        self.fodder = self.params['fodder']


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

    island.adding_animals([{'loc': (2, 2), 'pop': ani_pop}])

    year = 0
    for i in range(1000):
        print("Year: " + str(year))
        island.tile_update()
        for tile_row in island.tiles_lists:
            for tile in tile_row:
                if tile.can_move:
                    print("Tile: " + str(tile.grid_pos))
                    print("Carn: " + str(tile.carn.__len__()))
                    print("Herb: " + str(tile.herb.__len__()))
        year += 1

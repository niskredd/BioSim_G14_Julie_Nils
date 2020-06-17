
# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''

from biosim.landscape import *


class Island:

    def __init__(self, map):
        """
        Uses the data from the constructor to create the island, the string is
        converted to a list of tiles
        :param map: string
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

    def rgb_for_map(self, input_raw_string):
        """
        Takes the string of the map and adds color to the map
        :param input_raw_string: string
        :return: list of colors
        """
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                    for row in input_raw_string.splitlines()]

        return map_rgb

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
        for tile_row in self.tiles_lists:
            for tile in tile_row:
                for neighbour in neighbour_coordinates:
                    if tile.grid_pos == neighbour:
                        neighbours.append(tile)
        return neighbours

    def migrate(self, tile):
        """
        Handles the migration and moves animals between tiles, this also makes sure no one moves
        twice.
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

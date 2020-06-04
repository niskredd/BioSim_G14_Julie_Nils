
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
        self.num_herb = 0
        self.num_carn = 0
        self.fodder = 0

    def update_num_animals(self):
        return (self.num_carn, self.num_herb)

    def update_fodder_amount(self):
        self.fodder = 800 # given highland

    def fodder_per_herb(self):
        return self.fodder / self.num_herb

class


class Highland(Tile):
    """

    """
    def amount_fodder(self):






if __name__ == '__main__':
    pass

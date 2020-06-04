
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
        self.fodder = 0

    def update_num_animals(self):
        return len(self.num_carn), len(self.num_herb)

    def update_fodder_amount(self):
        self.fodder = 800  # given highland

    def fodder_per_herb(self):
        return self.fodder / self.num_herb

    def fauna(self, species, age, weight):
        self.herb.append(Herbivore)

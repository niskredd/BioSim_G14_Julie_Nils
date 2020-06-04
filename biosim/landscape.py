from .animal import *

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

    def birth(self, animal):
        if animal.w < animal.params['zeta'](animal.params['w_birth'] + animal.params['sigma_birth']):
            return None
        else:
            prob = min(1, animal.params['gamma'] * animal.phi * (animal.herb.__len__() - 1))
            if random.rand() < prob:
                new_born = Herbivore(0, 0)
                animal.w = new_born.w * animal.params['zeta']

                return new_born
            else:
                return None

    def death(self):
        if self.w == 0:
            return True
        else:
            probability = self.params['omega'] * (1 - self.phi)
            if random.rand() < probability:
                return False
            else:
                return True

if __name__ == '__main__':
    mini_map = Tile((1, 1))

    mini_map.fauna('Herbivore', 10, 12.5)
    mini_map.fauna('Herbivore', 9, 10.5)

    while 1:
        """
        eat
        update animal info
        birth
        """
        new = mini_map.birth(mini_map.herb[0])
        if new is not None:
            mini_map.herb.append(new)

        """
        death
        
        update fodder
        """

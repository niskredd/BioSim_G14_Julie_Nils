
class Tile:

    def __init__(self, grid_pos, food):
        self.grid_pos = grid_pos
        self.num_herb = 0
        self.num_carn = 0
        self.food_in_tile = food

    def update_num_aninmals(self):
        pass

    def update_food_amount(self):
        pass

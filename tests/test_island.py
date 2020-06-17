
import pytest
from biosim.island import Island, Water


class TestIsland:

    @pytest.fixture()
    def create_island(self):
        return Island("WWW\nWDW\nWWW")

    def test_tiles_list(self, create_island):
        island = create_island
        assert island.tiles_lists.__len__() == 3
        assert isinstance(island.tiles_lists[0][0], Water)

    def test_map_test(self, create_island):
        create_island.map_test("")


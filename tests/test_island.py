
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
        tile = create_island
        with pytest.raises(ValueError):
            assert tile.map_test("DWWWHWWWW")
            assert tile.map_test("WWWDWWWWW")
            assert tile.map_test("WWWWWDWWW")

    def test_size_test(self):
        with pytest.raises(ValueError):
            assert Island("WWWWDDDWWW").size_test()







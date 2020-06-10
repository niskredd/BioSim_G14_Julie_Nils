
import pytest
from biosim.landscape import Island

class Test_Island:

    @pytest.fixture()
    def create_island(self):
        return Island("WWW\nWDW\nWWW")

    def test_create_island(self, create_island):
        create_island.create_island()

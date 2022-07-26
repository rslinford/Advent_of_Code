import unittest

class GameBoard:
    def __init__(self):
        self.board = [[Tile(), Tile(), Tile(), Tile(), Tile()],
                      [Tile(), Tile(), Tile(), Tile(), Tile()],
                      [Tile(), Tile(), Tile(), Tile(), Tile()],
                      [Tile(), Tile(), Tile(), Tile(), Tile()],
                      [Tile(), Tile(), Tile(), Tile(), Tile()]]
    def __repr__(self):
        return f'GameBoard(\n{self.render()})'

    def render(self):
        rval = []
        for i, row in enumerate(self.board):
            for tile in row:
                rval.append(f'{tile.number:2} ')
            if i < 4:
                rval.append('\n')
        return ''.join(rval)


class Tile:
    def __init__(self, number = 0, marked=False):
        self.number = number
        self.marked = marked
    def __repr__(self):
        return f'Tile({self.number}, {self.marked})'


class TestGameBoard(unittest.TestCase):
    def test_game_board(self):
        gb = GameBoard()
        self.assertEqual(0, str(gb).find('GameBoard'))
        print(gb)

class TestTile(unittest.TestCase):
    def test_tile(self):
        self.assertEqual(0, str(Tile()).find('Tile'))

if __name__ == '__main__':
    unittest.main()


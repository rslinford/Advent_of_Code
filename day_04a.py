import unittest

from colorama import init

init()
from termcolor import colored


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
                if tile.marked:
                    rval.append(colored(f'{tile.number:2} ', 'green', 'on_grey'))
                else:
                    rval.append(f'{tile.number:2} ')
                if tile.marked:
                    rval.append('\033[0m')
            if i < 4:
                rval.append('\n')
        return ''.join(rval)

    def initialize_from_text_grid(self, text_grid):
        parsed_text_grid = text_grid.replace('\n', ' ').replace('  ', ' ').split(' ')
        if (len(parsed_text_grid) != 25):
            raise Exception(f'Text grid wrong length ({len(parsed_text_grid)}) expected 25')
        row, col = 0, 0
        for x in parsed_text_grid:
            self.board[row][col].number = int(x)
            col += 1
            if col > 4:
                col = 0
                row += 1


class Tile:
    def __init__(self, number=0, marked=False):
        self.number = number
        self.marked = marked

    def __repr__(self):
        return f'Tile({self.number}, {self.marked})'


class TestGameBoard(unittest.TestCase):
    def test_game_board(self):
        gb = GameBoard()
        self.assertEqual(0, str(gb).find('GameBoard'))
        gb.board[0][0].number = 21
        gb.board[1][1].number = 22
        gb.board[1][1].marked = True
        gb.board[2][2].number = 23
        gb.board[3][3].number = 24
        self.assertEqual(21, gb.board[0][0].number)
        self.assertFalse(gb.board[0][0].marked)
        self.assertEqual(22, gb.board[1][1].number)
        self.assertTrue(gb.board[1][1].marked)

    def test_initialize_from_text_grid(self):
        gb = GameBoard()
        gb.initialize_from_text_grid(
"""66 78  7 45 92
39 38 62 81 77
9 73 25 97 99
87 80 19  1 71
85 35 52 26 68""")
        self.assertEqual(66, gb.board[0][0].number)
        self.assertEqual(68, gb.board[4][4].number)

class TestTile(unittest.TestCase):
    def test_tile(self):
        self.assertEqual(0, str(Tile()).find('Tile'))


if __name__ == '__main__':
    unittest.main()

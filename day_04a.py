from colorama import init
init()
import time
import unittest
from termcolor import colored


class GameRoom:
    def __init__(self):
        self.boards = []
        self.callouts = []

    def initialize_boards_from_file(self, filename):
        with open(filename, 'r') as f:
            text = f.read()
        for t in text.split('\n\n'):
            gb = GameBoard()
            gb.initialize_from_text_grid(t)
            self.boards.append(gb)

    def initialize_callout_list_from_file(self, filename):
        with open(filename, 'r') as f:
            list = f.read().strip().split(',')
            self.callouts = [int(x) for x in list]

    def call_out(self, number):
        bingos = []
        for i, gb in enumerate(self.boards):
            if gb.handle_call(number):
                if gb.is_winner():
                    bingos.append(gb)
        return bingos

    def play(self, boards_filename, callout_filename):
        self.initialize_boards_from_file(boards_filename)
        self.initialize_callout_list_from_file(callout_filename)
        for call in self.callouts:
            for board in self.boards:
                board.handle_call(call)
                if board.is_winner():
                    return board
        return None

class GameBoard:
    def __init__(self):
        self.board = [[Tile(), Tile(), Tile(), Tile(), Tile()],
                      [Tile(), Tile(), Tile(), Tile(), Tile()],
                      [Tile(), Tile(), Tile(), Tile(), Tile()],
                      [Tile(), Tile(), Tile(), Tile(), Tile()],
                      [Tile(), Tile(), Tile(), Tile(), Tile()]]
        self.winning_number = 0

    def __repr__(self):
        return f'GameBoard({self.render()})'

    def render(self):
        rval = []
        if self.winning_number:
            rval.append(colored(f'{self.calculate_score()}', 'red', 'on_white'))
            rval.append('\n')
        else:
            rval.append('\n')
        for i, row in enumerate(self.board):
            for tile in row:
                if tile.number == self.winning_number:
                    rval.append(colored(f'{tile.number:2} ', 'red', 'on_grey'))
                elif tile.marked:
                    rval.append(colored(f'{tile.number:2} ', 'green', 'on_grey'))
                else:
                    rval.append(f'{tile.number:2} ')
            if i < 4:
                rval.append('\n')
        return ''.join(rval)

    def initialize_from_text_grid(self, text_grid):
        text_grid = text_grid.strip()
        parsed_text_grid = text_grid.replace('\n', ' ').replace('  ', ' ').split(' ')
        if len(parsed_text_grid) != 25:
            raise Exception(f'Text grid wrong length ({len(parsed_text_grid)}) expected 25')
        row, col = 0, 0
        for x in parsed_text_grid:
            self.board[row][col].number = int(x)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def handle_call(self, tile_number):
        for row in range(5):
            for col in range(5):
                if self.board[row][col].number == tile_number:
                    self.board[row][col].marked = True
                    if self.is_winner():
                        self.winning_number = tile_number
                    return True # True if tile was marked
        return False

    def is_winner(self):
        # check for horizontal win
        for row in range(5):
            col_full = True
            for col in range(5):
                if not self.board[row][col].marked:
                    col_full = False
                    break
            if col_full:
                return True
        # check for vertical win
        for col in range(5):
            col_full = True
            for row in range(5):
                if not self.board[row][col].marked:
                    col_full = False
                    break
            if col_full:
                return True
        # check for diagonal win Upper Left to Lower Right
        diag_full = True
        for col in range(5):
            row = col
            if not self.board[row][col].marked:
                diag_full = False
                break
        if diag_full:
            return True
        # check for diagonal win Lower Left to Upper Right
        diag_full = True
        for col in range(5):
            row = 4 - col
            if not self.board[row][col].marked:
                diag_full = False
                break
        if diag_full:
            return True
        return False

    def calculate_score(self):
        if not self.winning_number:
            raise Exception(f'Cannot calculate score without a winning number {self}')
        sum = 0
        for row in range(5):
            for col in range(5):
                if not self.board[row][col].marked:
                    sum += self.board[row][col].number
        return self.winning_number * sum

class Tile:
    def __init__(self, number=0, marked=False):
        self.number = number
        self.marked = marked

    def __repr__(self):
        return f'Tile({self.number}, {self.marked})'


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.gb = GameBoard()
        self.gb.initialize_from_text_grid(
            "66 78  7 45 92\n"
            "39 38 62 81 77\n"
            "9 73 25 97 99\n"
            "87 80 19  1 71\n"
            "85 35 52 26 68")

    def test_game_board(self):
        self.assertEqual(0, str(self.gb).find('GameBoard'))
        self.gb.board[0][0].number = 21
        self.gb.board[1][1].number = 22
        self.gb.board[1][1].marked = True
        self.gb.board[2][2].number = 23
        self.gb.board[3][3].number = 24
        self.assertEqual(21, self.gb.board[0][0].number)
        self.assertFalse(self.gb.board[0][0].marked)
        self.assertEqual(22, self.gb.board[1][1].number)
        self.assertTrue(self.gb.board[1][1].marked)

    def test_initialize_from_text_grid(self):
        self.assertEqual(66, self.gb.board[0][0].number)
        self.assertEqual(68, self.gb.board[4][4].number)

    def test_handle_call(self):
        self.assertFalse(self.gb.handle_call(100))
        self.assertFalse(self.gb.board[2][2].marked)
        self.assertTrue(self.gb.handle_call(25))
        self.assertTrue(self.gb.board[2][2].marked)

    def test_is_winner(self):
        self.assertFalse(self.gb.is_winner())
        self.gb.board[0][0].marked = True
        self.gb.board[0][1].marked = True
        self.gb.board[0][2].marked = True
        self.gb.board[0][3].marked = True
        self.gb.board[0][4].marked = True
        self.assertTrue(self.gb.is_winner())
        self.gb.board[0][4].marked = False
        self.assertFalse(self.gb.is_winner())
        self.gb.board[0][0].marked = True
        self.gb.board[1][0].marked = True
        self.gb.board[2][0].marked = True
        self.gb.board[3][0].marked = True
        self.gb.board[4][0].marked = True
        self.assertTrue(self.gb.is_winner())
        self.gb.board[4][0].marked = False
        self.assertFalse(self.gb.is_winner())
        self.gb.board[1][1].marked = True
        self.gb.board[2][2].marked = True
        self.gb.board[3][3].marked = True
        self.gb.board[4][4].marked = True
        self.assertTrue(self.gb.is_winner())
        self.gb.board[0][0].marked = False
        self.assertFalse(self.gb.is_winner())
        self.gb.board[0][4].marked = True
        self.gb.board[1][3].marked = True
        self.gb.board[2][2].marked = True
        self.gb.board[3][1].marked = True
        self.gb.board[4][0].marked = True
        self.assertTrue(self.gb.is_winner())

    def test_calculate_score(self):
        self.gb.handle_call(85)
        self.gb.handle_call(35)
        self.gb.handle_call(52)
        self.gb.handle_call(26)
        self.gb.handle_call(68)
        self.assertTrue(self.gb.is_winner())
        self.assertEqual(68, self.gb.winning_number)
        score = self.gb.calculate_score()
        self.assertEqual(77928, score)


class TestTile(unittest.TestCase):
    def test_tile(self):
        self.assertEqual(0, str(Tile()).find('Tile'))


class TestGameRoom(unittest.TestCase):
    def test_game_room(self):
        gr = GameRoom()
        gr.initialize_boards_from_file('bingo_boards.txt')
        self.assertEqual(100, len(gr.boards))
        self.assertEqual(66, gr.boards[0].board[0][0].number)

    def test_call_out(self):
        gr = GameRoom()
        gr.initialize_boards_from_file('bingo_boards.txt')
        numbers = [66, 78, 7, 45, 92]
        for i, n in enumerate(numbers):
            bingos = gr.call_out(n)
            if i < 4:
                self.assertFalse(bingos)
            else:
                self.assertTrue(bingos)
        self.assertEqual(92, bingos[0].winning_number)

    def test_play(self):
        gr = GameRoom()
        winner = gr.play('bingo_boards.txt', 'bingo_calls.txt')
        self.assertTrue(winner)
        print(winner)

    def test_initialize_callout_list_from_file(self):
        gr = GameRoom()
        gr.initialize_callout_list_from_file('bingo_calls.txt')
        self.assertEqual(37, gr.callouts[0])
        self.assertEqual(60, gr.callouts[1])
        self.assertEqual(79, gr.callouts[-1])

if __name__ == '__main__':
    unittest.main()

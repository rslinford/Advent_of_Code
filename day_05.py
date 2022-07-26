import unittest


class GridBoard:
    def __init__(self, size):
        self.grid = None
        self.size = size

    def reset_grid(self):
        self.grid =[[0 for _ in range(self.size)] for _ in range(self.size)]

    def render_grid(self):
        pass

class Line:
    def __init__(self):
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0


class TestGridBoard(unittest.TestCase):
    def test_init(self):
        gb = GridBoard(10)
        self.assertEqual(10, gb.size)
        self.assertEqual(None, gb.grid)

    def test_reset_grid(self):
        gb = GridBoard(10)
        gb.reset_grid()
        self.assertEqual(0, gb.grid[0][0])
        self.assertEqual(0, gb.grid[9][9])
        with self.assertRaises(IndexError):
            _ = gb.grid[10][0]
        with self.assertRaises(IndexError):
            _ = gb.grid[0][10]




if __name__ == '__main__':
    unittest.main()

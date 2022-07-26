import unittest


class GridBoard:
    def __init__(self, size):
        self.grid = None  # initialized in reset_grid()
        self.size = size
        self.reset_grid()

    def __repr__(self):
        return self.render_grid()

    def reset_grid(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def render_grid(self):
        rval = []
        for row in self.grid:
            for int_value in row:
                if not int_value:
                    rval.append('.')
                else:
                    rval.append(str(int_value))
            rval.append('\n')
        return ''.join(rval)


class Line:
    def __init__(self):
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0


class TestGridBoard(unittest.TestCase):
    def test_init(self):
        gb = GridBoard(10)
        self.assertEqual(10, gb.size)
        self.assertNotEqual(None, gb.grid)

    def test_reset_grid(self):
        gb = GridBoard(10)
        self.assertEqual(0, gb.grid[0][0])
        self.assertEqual(0, gb.grid[9][9])
        with self.assertRaises(IndexError):
            _ = gb.grid[10][0]
        with self.assertRaises(IndexError):
            _ = gb.grid[0][10]

    def test_render_grid(self):
        gb = GridBoard(3)
        self.assertEqual('...\n...\n...\n', gb.render_grid())
        gb.grid[0][0] = 1
        gb.grid[2][2] = 2
        self.assertEqual('1..\n...\n..2\n', gb.render_grid())
        print(gb)


if __name__ == '__main__':
    unittest.main()

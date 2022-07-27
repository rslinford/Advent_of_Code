import unittest


class GridBoard:
    def __init__(self, size):
        self.grid = None  # initialized in reset_grid()
        self.size = size
        self.reset_grid()

    def __repr__(self):
        return self.render_grid()

    def initialize_grid_from_file(self, filename, include_diagonals=False):
        self.reset_grid()
        with open(filename, 'r') as f:
            for text_line in f:
                text_line = text_line.strip()
                line = Line().initialize_from_string(text_line)

                if line.is_diagonal() and not include_diagonals:
                    continue
                self.draw_line_on_grid(line)

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

    def draw_line_on_grid(self, line):
        x = line.x1
        y = line.y1

        xstep = 0
        if line.x1 - line.x2 > 0:
            xstep = -1
        elif line.x1 - line.x2 < 0:
            xstep = 1
        ystep = 0
        if line.y1 - line.y2 > 0:
            ystep = -1
        elif line.y1 - line.y2 < 0:
            ystep = 1

        self.grid[y][x] += 1
        # special case: a line that is also a point
        if xstep == 0 and ystep == 0:
            return
        while True:
            x += xstep
            y += ystep
            # grid border checking
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                return
            self.grid[y][x] += 1
            # check for line's end point
            if x == line.x2 and y == line.y2:
                return

    def calculate_grid_score(self):
        score = 0
        for row in self.grid:
            for value in row:
                if value > 1:
                    score += 1
        return score


class Line:
    def __init__(self):
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0

    def __repr__(self):
        return f'Line({self.x1},{self.y1} -> {self.x2},{self.y2})'

    # Sample text_line: 0,9 -> 5,9
    def initialize_from_string(self, text_line):
        line = text_line.replace(',', ' ').replace('-', '').replace('>', '').replace('  ', ' ').split(' ')
        self.x1 = int(line[0])
        self.y1 = int(line[1])
        self.x2 = int(line[2])
        self.y2 = int(line[3])
        return self

    def is_diagonal(self):
        # Special case: line that's also a point that we
        # will treat as if not diagonal
        if self.x1 == self.x2 and self.y1 == self.y2:
            return False
        return self.x1 != self.x2 and self.y1 != self.y2


class TestGridBoard(unittest.TestCase):
    def setUp(self):
        self.short_rendered_gridboard = (".......1..\n"
                                         "..1....1..\n"
                                         "..1....1..\n"
                                         ".......1..\n"
                                         ".112111211\n"
                                         "..........\n"
                                         "..........\n"
                                         "..........\n"
                                         "..........\n"
                                         "222111....\n")
        self.short_rendered_gridboard_diagonal = ("1.1....11.\n"
                                                  ".111...2..\n"
                                                  "..2.1.111.\n"
                                                  "...1.2.2..\n"
                                                  ".112313211\n"
                                                  "...1.2....\n"
                                                  "..1...1...\n"
                                                  ".1.....1..\n"
                                                  "1.......1.\n"
                                                  "222111....\n")

    def test_init(self):
        gb = GridBoard(10)
        self.assertEqual(10, gb.size)
        self.assertNotEqual(None, gb.grid)

    def test_initialize_grid_from_file(self):
        gb = GridBoard(10)
        gb.initialize_grid_from_file('vent_lines_short.txt')
        self.assertEqual(self.short_rendered_gridboard, str(gb))
        gb.initialize_grid_from_file('vent_lines_short.txt', include_diagonals=True)
        self.assertEqual(self.short_rendered_gridboard_diagonal, str(gb))

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

    def test_calculate_grid_score(self):
        gb = GridBoard(10)
        gb.initialize_grid_from_file('vent_lines_short.txt')
        self.assertEqual(5, gb.calculate_grid_score())

    def test_for_real_this_time(self):
        gb = GridBoard(1000)
        gb.initialize_grid_from_file('vent_lines.txt', include_diagonals=True)
        print(gb.calculate_grid_score())


class TestLine(unittest.TestCase):
    def test_init(self):
        a = Line()
        self.assertEqual(0, a.x1)
        self.assertEqual(0, a.y1)
        self.assertEqual(0, a.x2)
        self.assertEqual(0, a.y2)

    def test_repr(self):
        a = Line()
        self.assertEqual(0, str(a).find('Line'))
        self.assertEqual(')', str(a)[-1])
        self.assertNotEqual(-1, str(a).find('->'))

    def test_draw_line_on_grid(self):
        line = Line()
        gb = GridBoard(3)
        gb.draw_line_on_grid(line)
        self.assertEqual('1..\n...\n...\n', str(gb))
        line.x1, line.y1, line.x2, line.y2 = 2, 0, 2, 2
        gb.draw_line_on_grid(line)
        self.assertEqual('1.1\n..1\n..1\n', str(gb))

    def test_initialize_from_string(self):
        line = Line()
        line.initialize_from_string('0,9 -> 5,9')
        self.assertEqual(0, line.x1)
        self.assertEqual(9, line.y1)
        self.assertEqual(5, line.x2)
        self.assertEqual(9, line.y2)

    def test_is_diagonal(self):
        line = Line()
        self.assertFalse(line.is_diagonal())
        line.x1, line.y1, line.x2, line.y2 = 0, 0, 3, 3
        self.assertTrue(line.is_diagonal())


if __name__ == '__main__':
    unittest.main()

import unittest

short = True
filename = 'octopus_short.txt' if short else 'octopus.txt'


def read_octopus_grid():
    octopus_grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            octopus_grid.append([int(c) for c in line])
    return octopus_grid


og = read_octopus_grid()
width = len(og[0])
height = len(og)


def render_octopus_grid(grid):
    rval = []
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            rval.append(str(value))
        rval.append('\n')

    return ''.join(rval)


def increase_by_one(og):
    for y, row in enumerate(og):
        for x, value in enumerate(row):
            og[y][x] += 1
            if og[y][x] > 9:
                og[y][x] = 0


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f'({self.x}, {self.y})'
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash(self.x + self.y)

def increase_adjacent_by_one(og, coor, been_there=None):
    if coor in been_there:
        return
    been_there.add(coor)
    # Up
    if coor.y > 0:
        og[coor.y - 1][coor.x] += 1
        if og[coor.y - 1][coor.x] > 9:
            increase_adjacent_by_one(coor.y - 1, coor.x, been_there)
    # Down
    if coor.y < height - 1:
        og[coor.y + 1][coor.x] += 1
        if og[coor.y + 1][coor.x] > 9:
            increase_adjacent_by_one(coor.y + 1, coor.x, been_there)

    # Left
    if coor.x > 0:
        og[coor.y][coor.x - 1] += 1
        if og[coor.y][coor.x - 1] > 9:
            increase_adjacent_by_one(coor.y, coor.x - 1, been_there)
    # Right
    if coor.x < width - 1:
        og[coor.y][coor.x + 1] += 1
        if og[coor.y][coor.x + 1] > 9:
            increase_adjacent_by_one(coor.y, coor.x + 1, been_there)


been_there = set()
og = read_octopus_grid()

#  1) octopus energies increase by 1
increase_by_one(og)
#  2) Any octopus greater than 9 flashes. A value of 0 is 'greater' because it stands for 10 at this point.
for y, row in enumerate(og):
    for x, value in enumerate(row):
        if og[y][x] == 0:
            increase_adjacent_by_one(og, Coordinates(x, y), been_there)

#  3) Adjacent octopuses increase by 1
#  4) Propagate flash adjacently with cycle detection
#  5) Octopuses that flashed set to 0


class TestOctopus(unittest.TestCase):
    def test_render_octopus_grid(self):
        og = read_octopus_grid()
        render = render_octopus_grid(og)
        if not short:
            self.assertEqual(0, render.find('5433566276'))
            self.assertTrue(render.find('5876712227') > 0)

    def test_increase_by_one(self):
        og = read_octopus_grid()
        if short:
            self.assertEqual('11111', ''.join([str(x) for x in og[0]]))
            self.assertEqual('19991', ''.join([str(x) for x in og[3]]))
            increase_by_one(og)
            self.assertEqual('22222', ''.join([str(x) for x in og[0]]))
            self.assertEqual('20002', ''.join([str(x) for x in og[3]]))


class TestCoordinates(unittest.TestCase):
    def test_coordinates(self):
        self.assertEqual('(0, 0)', str(Coordinates(0, 0)))
        self.assertEqual('(3, 5)', str(Coordinates(3, 5)))
        self.assertEqual(Coordinates(1, 33), Coordinates(1, 33))
        self.assertNotEqual(Coordinates(2, 33), Coordinates(1, 33))
        self.assertNotEqual(Coordinates(1, 34), Coordinates(1, 33))

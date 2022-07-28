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


#  1) octopus energies increase by 1
og = read_octopus_grid()
increase_by_one(og)

#  2) Any octopus greater than 9 flashes
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



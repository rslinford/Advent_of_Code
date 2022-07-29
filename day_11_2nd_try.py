from colorama import init
init()
from termcolor import colored
import unittest

short = True
filename = 'octopus_short.txt' if short else 'octopus.txt'


def read_octopus_grid(filename_override = None):
    octopus_grid = []
    a = filename_override if filename_override else filename
    with open(a, 'r') as f:
        for line in f:
            line = line.strip()
            octopus_grid.append([int(c) for c in line])
    return octopus_grid


def render_octopus_grid(grid, been_flashed=None, yar=None):
    rval = []
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if yar and x == yar.x and y == yar.y:
                rval.append(colored(f'{value:3}', 'green', 'on_grey'))
            elif been_flashed and Coordinates(x, y) in been_flashed:
                rval.append(colored(f'{value:3}', 'blue', 'on_grey'))
            else:
                rval.append(f'{value:3}')
        rval.append('\n')
    return ''.join(rval)


def increase_by_one(og):
    for y, row in enumerate(og):
        for x, value in enumerate(row):
            og[y][x] += 1


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


def flash_one(og, coor, been_flashed):
    width = len(og[0])
    height = len(og)

    if coor in been_flashed:
        return False

    been_flashed.add(coor)
    #  Up
    if coor.y > 0:
        og[coor.y - 1][coor.x] += 1
    # Down
    if coor.y < height - 1:
        og[coor.y + 1][coor.x] += 1
    # Left
    if coor.x > 0:
        og[coor.y][coor.x - 1] += 1
    # Right
    if coor.x < width - 1:
        og[coor.y][coor.x + 1] += 1
    # Upper Right
    if coor.x < width - 1 and coor.y > 0:
        og[coor.y - 1][coor.x + 1] += 1
    # Lower Right
    if coor.x < width - 1 and coor.y < height - 1:
        og[coor.y + 1][coor.x + 1] += 1
    # Lower Left
    if coor.x > 0 and coor.y < height - 1:
        og[coor.y + 1][coor.x - 1] += 1
    # Upper Left
    if coor.x > 0 and coor.y > 0:
        og[coor.y - 1][coor.x - 1] += 1
    return True


def simultaneous_flash_detection(og):
    for y, row in enumerate(og):
        for x, value in enumerate(row):
            if og[y][x] != 0:
                return False
    return True


def flash(og):
    been_flashed = set()
    flash_count = 0
    # Flash all that are over the limit
    while True:
        nothing_happened_this_round = True
        for y, row in enumerate(og):
            for x, value in enumerate(row):
                if og[y][x] > 9:
                    coor = Coordinates(x,y)
                    if flash_one(og, coor, been_flashed):
                        nothing_happened_this_round = False
                        flash_count += 1
                    if flash_count % 10 == 0:
                        print(f'After flash {coor}\n{render_octopus_grid(og, been_flashed, coor)}')
        if nothing_happened_this_round:
            break
        else:
            print('Round we go...')

    # Reset all that have been_flashed
    for coor in been_flashed:
        og[coor.y][coor.x] = 0

    if simultaneous_flash_detection(og):
        print(f'After simultaneous flash {coor}\n{render_octopus_grid(og, been_flashed, coor)}')
    return flash_count


class TestOctopus(unittest.TestCase):
    def test_render_octopus_grid(self):
        og = read_octopus_grid()
        render = render_octopus_grid(og)
        if not short:
            self.assertEqual(0, render.find('5433566276'))
            self.assertTrue(render.find('5876712227') > 0)

    def test_increase_by_one(self):
        og = read_octopus_grid()
        # print(f'Starting with\n{render_octopus_grid(og)}')
        self.assertEqual("  1  1  1  1  1\n"
                         "  1  9  9  9  1\n"
                         "  1  9  1  9  1\n"
                         "  1  9  9  9  1\n"
                         "  1  1  1  1  1\n", render_octopus_grid(og))
        increase_by_one(og)
        # print(f'After increase\n{render_octopus_grid(og)}')
        self.assertNotEqual("  2  2  2  2  2\n"
                            "  2  0  0  0  2\n"
                            "  2  0  2  0  2\n"
                            "  2  0  0  0  2\n"
                            "  2  2  2  2  2\n", render_octopus_grid(og))
    def test_flash(self):
        og = read_octopus_grid()
        increase_by_one(og)
        print(f'After increase\n{render_octopus_grid(og)}')
        flash(og)
        self.assertEqual("  3  4  5  4  3\n"
                         "  4  0  0  0  4\n"
                         "  5  0  0  0  5\n"
                         "  4  0  0  0  4\n"
                         "  3  4  5  4  3\n", render_octopus_grid(og))

    # def xtest_100_generations(self):
    #     og = read_octopus_grid('octopus_less_short.txt')
    #     print(f'Starting with\n{render_octopus_grid(og)}')
    #
    #     total_flashes = 0
    #     for generation in range(1, 101):
    #         increase_by_one(og)
    #         total_flashes += flash(og)
    #         print(f'After generation {generation} total flashes {total_flashes}\n{render_octopus_grid(og)}')
    #     self.assertEqual("  0  3  9  7  6  6  6  8  6  6\n"
    #                      "  0  7  4  9  7  6  6  9  1  8\n"
    #                      "  0  0  5  3  9  7  6  9  3  3\n"
    #                      "  0  0  0  4  2  9  7  8  2  2\n"
    #                      "  0  0  0  4  2  2  9  8  9  2\n"
    #                      "  0  0  5  3  2  2  2  8  7  7\n"
    #                      "  0  5  3  2  2  2  2  9  6  6\n"
    #                      "  9  3  2  2  2  2  8  9  6  6\n"
    #                      "  7  9  2  2  2  8  6  8  6  6\n"
    #                      "  6  7  8  9  9  9  8  7  6  6\n", render_octopus_grid(og))
    #     self.assertEqual(1656, total_flashes)

    def test_the_big_one(self):
        og = read_octopus_grid('octopus.txt')
        print(f'Starting with\n{render_octopus_grid(og)}')

        total_flashes = 0
        for generation in range(1, 300):
            increase_by_one(og)
            total_flashes += flash(og)
            print(f'After generation {generation} total flashes {total_flashes}\n{render_octopus_grid(og)}')


if __name__ == '__main__':
    unittest.main()



import time

from colorama import init

init()
from termcolor import colored

visited = set()
low_points = set()
basin = set()


def render_height_map(height_map, yar=None, been_there=None, lows=None):
    rval = []
    for y, row in enumerate(height_map):
        for x, value in enumerate(row):
            if yar and x == yar[0] and y == yar[1]:
                rval.append(colored(str(value), 'green', 'on_grey'))
            elif lows and (x, y) in lows:
                rval.append(colored(str(value), 'red', 'on_grey'))
            elif been_there and (x, y) in been_there:
                rval.append(colored(str(value), 'blue', 'on_grey'))
            else:
                rval.append(str(value))
        rval.append('\n')

    return ''.join(rval)


def visit_following_the_down(height_map, x, y):
    if (x, y) in visited:
        return
    visited.add((x, y))
    print(f'first time at {(x, y)}')
    if x % 50 == 0:
        print(render_height_map(height_map, (x, y), visited, low_points))

    visited_elsewhere = False
    # Up
    if y > 0 and height_map[y - 1][x] <= height_map[y][x]:
        visit_following_the_down(height_map, x, y - 1)
        visited_elsewhere = True
    # Down
    if y < height - 1 and height_map[y + 1][x] <= height_map[y][x]:
        visit_following_the_down(height_map, x, y + 1)
        visited_elsewhere = True
    # Left
    if x > 0 and height_map[y][x - 1] <= height_map[y][x]:
        visit_following_the_down(height_map, x - 1, y)
        visited_elsewhere = True
    # Right
    if x < width - 1 and height_map[y][x + 1] <= height_map[y][x]:
        visit_following_the_down(height_map, x + 1, y)
        visited_elsewhere = True
    if not visited_elsewhere:
        low_points.add((x,y))


def visit_following_the_up(height_map, x, y):
    if (x, y) in visited:
        return
    visited.add((x, y))
    print(f'first time at {(x, y)}')
    if x % 50 == 0:
        print(render_height_map(height_map, (x, y), basin, low_points))
    if height_map[y][x] != 9:
        basin.add((x,y))
    # Up
    if y > 0 and height_map[y - 1][x] >= height_map[y][x]:
        visit_following_the_up(height_map, x, y - 1)
    # Down
    if y < height - 1 and height_map[y + 1][x] >= height_map[y][x]:
        visit_following_the_up(height_map, x, y + 1)
    # Left
    if x > 0 and height_map[y][x - 1] >= height_map[y][x]:
        visit_following_the_up(height_map, x - 1, y)
    # Right
    if x < width - 1 and height_map[y][x + 1] >= height_map[y][x]:
        visit_following_the_up(height_map, x + 1, y)


short = False
filename = 'height_map_short.txt' if short else 'height_map.txt'

height_map = []
with open(filename) as f:
    for line in f:
        height_map.append([int(x) for x in line.strip()])

if short:
    assert (height_map[0][0] == 2)
    assert (height_map[4][9] == 8)

width = len(height_map[0])
height = len(height_map)

for y, row in enumerate(height_map):
    for x, value in enumerate(row):
        visit_following_the_down(height_map, x, y)
        # time.sleep(0.2)
print(low_points)

score = 0
for p in low_points:
    score += height_map[p[1]][p[0]] + 1
print(score)
# time.sleep(5.2)


basin_list = []
for p in low_points:
    visited.clear()
    basin.clear()
    visit_following_the_up(height_map, p[0], p[1])
    basin_list.append(basin.copy())
basin_list.sort(key=len, reverse=True)

score = len(basin_list[0]) * len(basin_list[1]) * len(basin_list[2])
print(f'The result is {score}')


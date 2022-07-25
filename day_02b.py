import unittest


def drive_commands(filename):
    with open(filename, 'r') as f:
        for line in f:
            drive_command = line.strip().split(' ')
            yield drive_command[0], int(drive_command[1])


def drive(filename):
    horizontal, depth, aim = 0, 0, 0
    for direction, distance in drive_commands(filename):
        match direction:
            case 'forward':
                horizontal += distance
                depth += aim * distance
            case 'down':
                aim += distance
            case 'up':
                aim -= distance
            case _:
                raise Exception(f'"{direction}" is not a valid direction')
    return horizontal, depth


class TestDrive(unittest.TestCase):
    def test_drive_commands(self):
        dc = drive_commands('submarine_directions_short_02.txt')
        x, y = next(dc)
        self.assertEqual('forward', x)
        self.assertEqual(8, y)
        for x, y in dc:
            pass
        self.assertEqual('up', x)
        self.assertEqual(9, y)

    def test_drive(self):
        horizontal, depth = drive('submarine_directions_short_02.txt')
        self.assertEqual(13, horizontal)
        self.assertEqual(88, depth)

        forward_distance, depth = drive('submarine_directions_02.txt')
        print(forward_distance, depth)
        print(forward_distance * depth)

"""
       horizontal  depth  aim
       ==========  =====  ===
               0     0     0
forward 8      8     0     0
forward 1      9     0     0
down 9         9     0     9
down 8         9     0    17
down 5         9     0    22
forward 4     13    88    22
up 9          13    88    13
"""

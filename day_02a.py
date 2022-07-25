import unittest

def drive_commands(filename):
    with open(filename, 'r') as f:
        for line in f:
            drive_command = line.strip().split(' ')
            yield drive_command[0], int(drive_command[1])

def drive(filename):
    forward_distance, depth = 0, 0
    for direction, distance in drive_commands(filename):
        match direction:
            case 'forward':
                forward_distance += distance
            case 'down':
                depth += distance
            case 'up':
                depth -= distance
            case _:
                raise Exception(f'"{direction}" is not a valid direction')
    return forward_distance, depth


class TestDriveCommands(unittest.TestCase):
    def test_directions(self):
        dc = drive_commands('submarine_directions_short_02.txt')
        direction, distance = next(dc)
        self.assertEqual('forward', direction)
        self.assertEqual(8, distance)
        direction, distance = next(dc)
        self.assertEqual('forward', direction)
        self.assertEqual(1, distance)
        direction, distance = next(dc)
        self.assertEqual('down', direction)
        self.assertEqual(9, distance)
        for direction, distance in dc:
            pass  # exhaust generator
        self.assertEqual('up', direction)
        self.assertEqual(9, distance)



    def test_drive(self):
        forward_distance, depth = drive('submarine_directions_short_02.txt')
        self.assertEqual(13, forward_distance)
        self.assertEqual(13, depth)
        forward_distance, depth = drive('submarine_directions_02.txt')
        print(forward_distance, depth)
        print(forward_distance * depth)



"""  from submarine_directions_short_02.txt
            forward_distance  depth
                  0             0
forward 8         8             0
forward 1         9             0
down 9            9             9
down 8            9            17
down 5            9            22
forward 4        13            22
up 9             13            13
"""

import unittest

def data_windows(file_name):
    with open(file_name, 'r') as f:
        readings = []
        for line in f:
            if len(readings) < 3:
                readings.append(int(line))
            else:
                yield tuple(readings)
                readings.pop(0)
                readings.append(int(line))
        yield tuple(readings)

def tally_increases(file_name):
    tally = 0
    a = None
    for window in data_windows(file_name):
        b = window
        if a and sum(b) > sum(a):
            tally += 1
        a = b
    return tally

""" Hand tallied from ocean_depths_short_01b.txt
188  572  x
191  576
193  578  x
192  565
193
180
          2 total increases
"""

class TestDataWindows(unittest.TestCase):
    def test_data_windows(self):
        dw = data_windows('ocean_depths_short_01b.txt')
        self.assertEqual(next(dw), (188, 191, 193))
        self.assertEqual(next(dw), (191, 193, 192))
        self.assertEqual(next(dw), (193, 192, 193))

        for x in dw:
            pass  #  Exhaust generator
        self.assertEqual(x, (192, 193, 180))

    def test_tally_increases(self):
        self.assertEqual(tally_increases('ocean_depths_short_01b.txt'), 2)
        print(tally_increases('ocean_depths.txt'))

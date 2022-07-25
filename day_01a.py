import unittest


def tally_increased(file_name):
    tally = 0
    with open(file_name, 'r') as f:
        a = None
        for line in f:
            b = int(line)
            if a and b > a:
                tally += 1
            a = b
    return tally

class TestTallyIncreased(unittest.TestCase):
    def test_tally_increased(self):
        self.assertEqual(tally_increased('ocean_depths_short_01a.txt'), 8)
        print(tally_increased('ocean_depths.txt'))

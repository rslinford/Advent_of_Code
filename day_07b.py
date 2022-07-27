import unittest


def read_crab_data(short=False):
    file_name = 'crabs_short.txt' if short else 'crabs.txt'
    with open(file_name, 'r') as f:
        text = f.read().strip()
    return list(map(int, text.split(',')))


def crab_move_cost(start_position, end_position):
    distance = abs(start_position - end_position)
    cost = sum_positive_integers(distance)
    return cost


def crab_swarm_move_cost(crabs, target_position):
    cost = 0
    for crab in crabs:
        cost += crab_move_cost(crab, target_position)
    return cost


def move_all_crabs_min_cost(crabs):
    min_cost = float('inf')
    for x in range(min(crabs), max(crabs) + 1):
        cost = crab_swarm_move_cost(crabs, x)
        if cost < min_cost:
            min_cost = cost
    return min_cost


def sum_positive_integers(upper_bound):
    sum = 0
    for n in range(1, upper_bound + 1):
        sum += n
    return sum


class TestCrabs(unittest.TestCase):
    def test_read_crab_data(self):
        self.assertEqual([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], read_crab_data(short=True))

    def test_crab_move_cost(self):
        self.assertEqual(1, crab_move_cost(1, 2))
        self.assertEqual(3, crab_move_cost(4, 2))
        self.assertEqual(10, crab_move_cost(5, 1))

    def test_crab_swarm_move_cost(self):
        crabs = read_crab_data(short=True)
        self.assertEqual(206, crab_swarm_move_cost(crabs, 2))

    def test_move_all_crabs_min_cost(self):
        crabs = read_crab_data(short=True)
        self.assertEqual(168, move_all_crabs_min_cost(crabs))
        crabs = read_crab_data(short=False)
        print(f'Min cost: {move_all_crabs_min_cost(crabs)}')

    def test_sum_positive_integers(self):
        self.assertEqual(1, sum_positive_integers(1))
        self.assertEqual(3, sum_positive_integers(2))
        self.assertEqual(10, sum_positive_integers(4))


if __name__ == '__main__':
    unittest.main()

import unittest


class CaveSystem:
    def __init__(self):
        self.start = Cave('start')
        self.end = Cave('end')
        self.caves = {self.start.name: self.start, self.end.name: self.end}

    def __repr__(self):
        return f'CaveSystem():\n{self.start}\n{self.end}'

    def render_system(self):
        rval = ['CaveSystem:\n']
        for cave in self.caves.values():
            if len(cave.neighbors) == 0:
                rval.append(f'{cave}\n')
            else:
                for neighbor in cave.neighbors:
                    rval.append(f'{cave} -> {neighbor}\n')
        return ''.join(rval)

    def add_connection(self, left, right):
        if left not in self.caves.keys():
            self.caves[left] = Cave(left)
        if right not in self.caves.keys():
            self.caves[right] = Cave(right)
        self.caves[left].connect(self.caves[right])

    def directly_connected(self, a, b):
        return self.caves[a].is_neighbor(b)

    def visit(self, name, visited, path):
        if name in visited.keys():
            visited[name] += 1
        else:
            visited[name] = 1
        if not self.caves[name].deja_vu_allowed() and visited[name] > 1:
            return

        path.append(name)
        if name == 'end':
            print('We have arrived.')
            return

        # Begin exploration
        print(f'Exploring {self.caves[name]}  path {path}')
        for cave in self.caves[name].neighbors.values():
            self.visit(cave.name, visited, path)

    def traverse(self):
        self.visit(self.start.name, dict(), [])

def load_cave_system_from_file(filename):
    cs = CaveSystem()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            a = line.split('-')
            left = a[0]
            right = a[1]
            cs.add_connection(left, right)
    return cs


class Cave:
    name: str

    def __init__(self, name):
        self.name = name
        self.neighbors = {}

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'Cave({self.name})'

    def connect(self, b):
        self.neighbors[b.name] = b
        b.neighbors[self.name] = self

    def directly_connected(self, cave_name):
        return cave_name in self.neighbors.keys()

    def render_connections(self):
        rval = [f'{self} connections:\n']
        for cave in self.neighbors:
            rval.append(f'{cave}\n')
        return ''.join(rval)

    def is_neighbor(self, cave_name):
        return cave_name in self.neighbors.keys()

    def deja_vu_allowed(self):
        # Two special cases
        if self.name == 'start' or self.name == 'end':
            return False
        return self.name.isupper()


class TestCave(unittest.TestCase):
    def test_init(self):
        cave = Cave('A')
        self.assertEqual('A', cave.name)

    def test_connect(self):
        a = Cave('a')
        b = Cave('b')
        a.connect(b)

    def test_directly_connected(self):
        a = Cave('a')
        b = Cave('b')
        self.assertFalse(a.directly_connected('b'))
        a.connect(b)
        self.assertTrue(a.directly_connected('b'))
        self.assertTrue(b.directly_connected('a'))

    def test_eq(self):
        a = Cave('A')
        self.assertEqual(a, a)
        b = Cave('B')
        self.assertNotEqual(a, b)
        other_a = Cave('A')
        self.assertEqual(a, other_a)

    def test_repr(self):
        a = Cave('Start')
        self.assertEqual(0, str(a).find('Cave'))

    def test_render_connections(self):
        a = Cave('a')
        b = Cave('b')
        c = Cave('start')
        a.connect(c)
        a.connect(b)
        rendered = a.render_connections()
        self.assertTrue(rendered)
        self.assertEqual(0, rendered.find('Cave'))
        self.assertNotEqual(-1, rendered.find('start'))

    def test_deja_vu_allowed(self):
        a = Cave('a')
        B = Cave('B')
        self.assertFalse(a.deja_vu_allowed())
        self.assertTrue(B.deja_vu_allowed())
        start = Cave('start')
        end = Cave('end')
        self.assertFalse(start.deja_vu_allowed())
        self.assertFalse(end.deja_vu_allowed())


class TestCaveSystem(unittest.TestCase):
    def test_cave_system(self):
        cs = CaveSystem()
        self.assertEqual(0, str(cs).find('CaveSystem'))
        self.assertNotEqual(-1, str(cs).find('start'))
        self.assertNotEqual(-1, str(cs).find('end'))

    def test_load_cave_system_from_file(self):
        cs = load_cave_system_from_file('cave_map_small.txt')
        self.assertTrue(cs)
        rendered = cs.render_system()
        self.assertNotEqual(-1, rendered.find('Cave(A)'))
        self.assertNotEqual(-1, rendered.find('Cave(b)'))
        self.assertTrue(cs.directly_connected('A', 'b'))
        self.assertTrue(cs.directly_connected('b', 'A'))
        self.assertFalse(cs.directly_connected('A', 'B'))

    def test_add_connection(self):
        cs = CaveSystem()
        cs.add_connection('a', 'b')

    def test_directly_connected(self):
        cs = CaveSystem()
        cs.add_connection('a', 'b')
        self.assertTrue(cs.directly_connected('a', 'b'))
        self.assertFalse(cs.directly_connected('a', 'c'))

    def test_render_system(self):
        cs = load_cave_system_from_file('cave_map_small.txt')
        rendered = cs.render_system()
        self.assertNotEqual('-1', rendered.find('Cave(A) -> b'))
        self.assertNotEqual('-1', rendered.find('Cave(b) -> end'))

    def test_traverse(self):
        cs = load_cave_system_from_file('cave_map_small.txt')
        cs.traverse()

import unittest
from collections import deque
from queue import SimpleQueue


def parse_line(text):
    queue = SimpleQueue()
    for c in text:
        match c:
            case '{' | '(' | '<' | '[':
                queue.put(c)
            case '}' | ')' | '>' | ']':
                if queue.qsize() == 0:
                    # c is an unmatched closing symbol
                    return False
                lefty = queue.get(block=False)
                match lefty:
                    case '{':
                        if c != '}':
                            return False
                    case '(':
                        if c != ')':
                            return False
                    case '<':
                        if c != '>':
                            return False
                    case '[':
                        if c != ']':
                            return False
    # Unmatched closing symbol(s) left over
    if queue.qsize() > 0:
        return False
    return True


short = True
filename = 'subsystem_short.txt' if short else 'subsystem.txt'
with open(filename, 'r') as f:
    for line in f:
        parse_line(line.strip())

class TestParser(unittest.TestCase):
    def test_parser(self):
        self.assertTrue(parse_line(''))
        self.assertTrue(parse_line('()'))
        self.assertTrue(parse_line('[]'))
        self.assertTrue(parse_line('{}'))
        self.assertTrue(parse_line('<>'))
        self.assertFalse(parse_line('('))
        self.assertFalse(parse_line(')'))
        self.assertFalse(parse_line(']'))
        self.assertFalse(parse_line('}'))
        self.assertFalse(parse_line('>'))
        self.assertTrue(parse_line('(((())))'))
        self.assertFalse(parse_line('(((())>))'))

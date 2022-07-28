import unittest
from queue import SimpleQueue, LifoQueue


def parse_line(text):
    queue = LifoQueue()
    for c in text:
        match c:
            case '{' | '(' | '<' | '[':
                queue.put_nowait(c)
            case '}' | ')' | '>' | ']':
                if queue.empty():
                    # c is an unmatched closing symbol
                    return False, c
                lefty = queue.get_nowait()
                match lefty:
                    case '{':
                        if c != '}':
                            return False, c
                    case '(':
                        if c != ')':
                            return False, c
                    case '<':
                        if c != '>':
                            return False, c
                    case '[':
                        if c != ']':
                            return False, c
    # Unmatched closing symbol(s) left over
    if not queue.empty():
        return False, queue.get_nowait()
    return True, ''

scoring_table = {')': 3, ']': 57, '}': 1197, '>': 25137}

short = False
filename = 'subsystem_short.txt' if short else 'subsystem.txt'
score = 0
with open(filename, 'r') as f:
    for line in f:
        correct, c = parse_line(line.strip())
        if not correct:
            worth = scoring_table.get(c)
            if worth:
                score += worth
print(score)
if short:
    assert(score == 26397)
else:
    'Answer ^^^'

class TestParser(unittest.TestCase):
    def test_parser(self):
        self.assertTrue(parse_line('')[0])
        self.assertTrue(parse_line('()')[0])
        self.assertTrue(parse_line('[]')[0])
        self.assertTrue(parse_line('{}')[0])
        self.assertTrue(parse_line('<>')[0])
        self.assertFalse(parse_line('(')[0])
        self.assertFalse(parse_line(')')[0])
        self.assertFalse(parse_line(']')[0])
        self.assertFalse(parse_line('}')[0])
        self.assertFalse(parse_line('>')[0])
        self.assertTrue(parse_line('(((())))')[0])
        self.assertFalse(parse_line('(((())>))')[0])
        self.assertFalse(parse_line('}((((<{[]}>))))')[0])
        self.assertTrue(parse_line('()()')[0])
        self.assertTrue(parse_line('(()())')[0])
        correct, c = parse_line('>[()]')
        self.assertEqual('>', c)
        self.assertFalse(correct)
        correct, c = parse_line('[()]}')
        self.assertEqual('}', c)
        self.assertFalse(correct)
        correct, c = parse_line('[()]{')
        self.assertEqual('{', c)
        self.assertFalse(correct)
        correct, c = parse_line('[]{}<>()')
        self.assertEqual('', c)
        self.assertTrue(correct)

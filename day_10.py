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
        left_overs = []
        while not queue.empty():
            left_overs.insert(0, queue.get_nowait())
        return True, ''.join(left_overs)
    return True, ''

def score_the_leftovers(leftovers):
    total_score = 0
    for c in leftovers:
        total_score *= 5
        match c:
            case '(' | ')':
                total_score += 1
            case '[' | ']':
                total_score += 2
            case '{' | '}':
                total_score += 3
            case '<' | '>':
                total_score += 4

    return total_score

def compose_completion_string(left_overs):
    rval = []
    for c in left_overs[::-1]:
        match c:
            case '(':
                rval.append(')')
            case '[':
                rval.append(']')
            case '{':
                rval.append('}')
            case '<':
                rval.append('>')

    return ''.join(rval)

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
    print('Answer ^^^')

score_list = []
with open(filename, 'r') as f:
    for line in f:
        line = line.strip()
        correct, left_overs = parse_line(line)
        if not correct:
            continue
        s = score_the_leftovers(compose_completion_string(left_overs))
        score_list.append(s)
        # print(line, left_overs, s)

score_list.sort()
print(score_list)
print(f'The middle score {score_list[len(score_list) // 2]}')


class TestParser(unittest.TestCase):
    def test_compose_completion_string(self):
        self.assertEqual('])}>', compose_completion_string('<{(['))
        self.assertEqual(']', compose_completion_string('['))

    def test_score_the_leftovers(self):
        self.assertEqual(288957, score_the_leftovers('}}]])})]'))
        self.assertEqual(5566, score_the_leftovers(')}>]})'))
        self.assertEqual(1480781, score_the_leftovers('}}>}>))))'))
        self.assertEqual(995444, score_the_leftovers(']]}}]}]}>'))
        self.assertEqual(294, score_the_leftovers('])}>'))

    def test_parser(self):
        self.assertTrue(parse_line('')[0])
        self.assertTrue(parse_line('()')[0])
        self.assertTrue(parse_line('[]')[0])
        self.assertTrue(parse_line('{}')[0])
        self.assertTrue(parse_line('<>')[0])
        self.assertTrue(parse_line('(')[0])
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
        self.assertTrue(correct)
        correct, c = parse_line('[]{}<>()')
        self.assertEqual('', c)
        self.assertTrue(correct)


import unittest
from collections import defaultdict


class SignalEntry:
    def __init__(self, patterns, output):
        self.patterns = patterns
        self.output = output
    def __repr__(self):
        return str(self.patterns) + str(self.output)


def sort_sort_list(item_list):
    """

    :type x: list
    """
    rval = []
    for item in item_list:
        rval.append(''.join(sorted(item)))
    rval = sorted(rval)
    return rval

def load_signal_data(short=False):
    filename = 'signals_short_08.txt' if short else 'signals_08.txt'
    entries = []
    with open(filename, 'r') as f:
        for line in f:
            pattern_text, output_text = line.strip().split(' | ')
            patterns = sort_sort_list(pattern_text.split(' '))
            output = sort_sort_list(output_text.split(' '))
            entries.append(SignalEntry(patterns, output))
    return entries

def def_value():
    return 0

def render_dict_sorted(d):
    """
    :type d: dict
    """
    rval = []
    rval.append('{')
    for i, key in enumerate(sorted(d.keys())):
        # print(key, d.get(key))
        if i > 0:
            rval.append(', ')
        rval.append(str(key))
        rval.append(': ')
        rval.append(str(d.get(key)))
    rval.append('}')
    return ''.join(rval)

def tally_output_lengths(entries):
    d = defaultdict(def_value)
    for entry in entries:
        for x in entry.output:
            d[len(x)] += 1
        # print(entry, d.items())
    return d

def tally_pattern_lengths(entry):
    d = defaultdict(def_value)
    for x in entry.patterns:
        d[len(x)] += 1
    return d


#    Easy numbers: 1, 4, 7, 8
#  Unique lengths: 2, 4, 3, 7

def sum_unique_length(lengths):
    return lengths[2] + lengths[3] + lengths[4] + lengths[7]


class TestSignalEntry(unittest.TestCase):
    def test_load_signal_data(self):
        entries = load_signal_data(True)
        self.assertTrue(entries)
        self.assertTrue(entries[0].patterns)
        self.assertTrue(entries[0].output)
        self.assertEqual(10, len(entries[0].patterns))
        self.assertEqual(4, len(entries[0].output))
        self.assertEqual(-1, entries[0].output[3].find('\n'))

    def test_tally_lengths(self):
        entries = load_signal_data(True)
        lengths = tally_output_lengths(entries)
        # print(f'2: {lengths[2]}, 3: {lengths[3]}, 4: {lengths[4]}, 7: {lengths[7]}   sum: {sum_unique_length(lengths)}')
        self.assertEqual(26, sum_unique_length(lengths))

    def test_tally_pattern_length(self):
        entries = load_signal_data(False)
        for entry in entries:
            lengths = tally_pattern_lengths(entry)
            # print(f'{lengths} : {entry}')
            # print(render_dict_sorted(lengths), entry)
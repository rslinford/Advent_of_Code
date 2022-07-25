import unittest

import numpy as np


def diagnostics(filename):
    with open(filename, 'r') as f:
        for line in f:
            diagnostic = line.strip()
            yield diagnostic


def make_zero_digit_tally(digit_width):
    zdt = []
    for i in range(digit_width):
        zdt.append([0, 0])
    return zdt


def tally_the_digits(filename, digit_width):
    dt = make_zero_digit_tally(digit_width)
    for diag in diagnostics(filename):
        for i in range(digit_width):
            if diag[i] == '0':
                dt[i][0] += 1
            elif diag[i] == '1':
                dt[i][1] += 1
            else:
                raise Exception(f'"{diag[i]}" is not a valid digit value.')
        # print(diag, dt)
    return dt


def translate_tally_to_binary_string_value(digit_tally):
    digits = []
    for i in range(len(digit_tally)):
        if digit_tally[i][0] > digit_tally[i][1]:
            digits.append('0')
        elif digit_tally[i][0] < digit_tally[i][1]:
            digits.append('1')
        else:
            raise Exception(f'Digit tally tie. What to do?')
    return ''.join(digits)


def flip_bits(binary_value):
    flipped = []
    for c in binary_value:
        if c == '0':
            flipped.append('1')
        elif c == '1':
            flipped.append('0')
        else:
            raise Exception(f'"{c}" is not a valid binary digit')
    return ''.join(flipped)


class TestDiagnostics(unittest.TestCase):
    def test_diagnostics(self):
        diag = diagnostics('diagnostic_short_03.txt')
        self.assertEqual('00100', next(diag))
        d = 0
        for d in diag:
            pass
        self.assertEqual('01010', d)

    def test_make_zero_digit_tally(self):
        zdt = make_zero_digit_tally(2)
        self.assertEqual(2, len(zdt))

        self.assertEqual(2, len(zdt[0]))
        self.assertEqual(0, zdt[0][0])
        self.assertEqual(0, zdt[0][1])

        self.assertEqual(2, len(zdt[1]))
        self.assertEqual(0, zdt[1][0])
        self.assertEqual(0, zdt[1][1])

    def test_tally_the_digits(self):
        dt = tally_the_digits('diagnostic_short_03.txt', 5)
        self.assertEqual(5, dt[0][0])
        self.assertEqual(7, dt[0][1])

        self.assertEqual(7, dt[1][0])
        self.assertEqual(5, dt[1][1])

        self.assertEqual(4, dt[2][0])
        self.assertEqual(8, dt[2][1])

        self.assertEqual(5, dt[3][0])
        self.assertEqual(7, dt[3][1])

        self.assertEqual(7, dt[4][0])
        self.assertEqual(5, dt[4][1])
        value = int(translate_tally_to_binary_string_value(dt), 2)
        self.assertEqual(22, value)
        return value

    def test_translate_tally_to_decimal_value(self):
        tally = [[5, 7], [7, 5], [4, 8], [5, 7], [7, 5]]  # 10110 -> 22
        value = int(translate_tally_to_binary_string_value(tally), 2)
        self.assertEqual(22, value)

    def test_flip_bits(self):
        self.assertEqual('1111', flip_bits('0000'))
        self.assertEqual('000', flip_bits('111'))
        self.assertEqual('010', flip_bits('101'))

    def test_for_real_this_time(self):
        dt = tally_the_digits('diagnostic_03.txt', 12)
        gama_rate_binary = translate_tally_to_binary_string_value(dt)
        epsilon_rate_binary = flip_bits(gama_rate_binary)
        print(gama_rate_binary, epsilon_rate_binary)
        gama_rate = int(gama_rate_binary, 2)
        epsilon_rate = int(epsilon_rate_binary, 2)
        print(gama_rate, epsilon_rate)
        print(gama_rate * epsilon_rate)


if __name__ == '__main__':
    unittest.main()

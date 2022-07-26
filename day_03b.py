import unittest


def diagnostics(filename):
    with open(filename, 'r') as f:
        for line in f:
            diagnostic = line.strip()
            yield diagnostic


def load_all_diagnostics(filename):
    return list(diagnostics(filename))

#  Keep diag items that have c at position index
def filter_by_bit(diag_list, c, index, inverse):
    keepers = []
    for d in diag_list:
        if not inverse:
            if d[index] == c:
                keepers.append(d)
        else:
            if d[index] != c:
                keepers.append(d)

    return keepers

def calculate_rates(filename, digit_width):
    diags = load_all_diagnostics(filename)
    tally = tally_the_digits(filename, digit_width)
    tally_binary = translate_tally_to_binary_string_value(tally)
    for i, c in enumerate(tally_binary):
        if c == '0':
            pass # then keep all with 0 in position i
        elif c == '1':
            pass # then keep all with 1 in position i
        else:
            raise Exception(f'"{c}" is not a valid binary number.')

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

def tally_the_digits_in_memory(diag_list, digit_width):
    dt = make_zero_digit_tally(digit_width)
    for diag in diag_list:
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
            # Tie goes to 1
            digits.append('1')
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

    def test_load_all_diagnostics(self):
        diag_list = load_all_diagnostics('diagnostic_short_03.txt')
        self.assertEqual(12, len(diag_list))
        self.assertEqual('00100', diag_list[0])
        self.assertEqual('01010', diag_list[11])

    def test_filter_by_bit(self):
        diag_list = load_all_diagnostics('diagnostic_short_03.txt')
        filtered_diag_list = filter_by_bit(diag_list, '0', 2, False)
        self.assertEqual(['10000', '11001', '00010', '01010'] ,
                         filtered_diag_list)
        filtered_diag_list = filter_by_bit(diag_list, '1', 4, False)
        self.assertEqual(['10111', '10101', '01111', '00111', '11001'],
                         filtered_diag_list)

    def test_run(self):
        diags = load_all_diagnostics('diagnostic_03.txt')
        dt = tally_the_digits_in_memory(diags, 12)
        bsv = translate_tally_to_binary_string_value(dt)
        for i in range(len(bsv)):
            diags = filter_by_bit(diags, bsv[i], i, False)
            if len(diags) < 2:
                break
            dt = tally_the_digits_in_memory(diags, 12)
            bsv = translate_tally_to_binary_string_value(dt)
        if len(diags) != 1:
            raise Exception(f'Was expecting len of 1 but found {len(diags)}')
        oxygen_generator_rating = int(diags[0], 2)
        # self.assertEqual(23, oxygen_generator_rating)

        diags = load_all_diagnostics('diagnostic_short_03.txt')
        dt = tally_the_digits_in_memory(diags, 5)
        bsv = translate_tally_to_binary_string_value(dt)
        for i in range(len(bsv)):
            diags = filter_by_bit(diags, bsv[i], i, True)
            if len(diags) < 2:
                break
            dt = tally_the_digits_in_memory(diags, 5)
            bsv = translate_tally_to_binary_string_value(dt)
        if len(diags) != 1:
            raise Exception(f'Was expecting len of 1 but found {len(diags)}')
        co2_scrubber_rating = int(diags[0], 2)
        # self.assertEqual(10, co2_scrubber_rating)

        print(oxygen_generator_rating, co2_scrubber_rating)



if __name__ == '__main__':
    unittest.main()

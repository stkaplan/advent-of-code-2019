#!/usr/bin/env python3

import unittest

start = 197487
end = 673251

def get_digits(num):
    digits = []
    while num > 0:
        num, digit = divmod(num, 10)
        digits.append(digit)
    return list(reversed(digits))

def check_number(num):
    # Don't need to check if it's a 6 digit number, or in range, because we
    # only try valid numbers here.
    has_double = False
    all_increasing = True
    digits = get_digits(num)
    for i in range(len(digits)-1):
        if digits[i] == digits[i+1]:
            has_double = True
        if digits[i] > digits[i+1]:
            all_increasing = False

        if has_double and not all_increasing:
            return False
    return has_double and all_increasing

class Test(unittest.TestCase):
    def test_check_number(self):
        self.assertTrue(check_number(111111))
        self.assertFalse(check_number(223450))
        self.assertFalse(check_number(123789))

if __name__ == '__main__':
    unittest.main(exit=False)

    num_matching = sum(1 for i in range(start, end+1) if check_number(i))
    print(num_matching)
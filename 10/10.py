#!/usr/bin/env python3

import math
import unittest
from collections import namedtuple

Position = namedtuple('Position', ['x', 'y'])

def read_file(filename):
    asteroids = []
    with open(filename) as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line.rstrip()):
                if char == '#':
                    asteroids.append(Position(x=j, y=i))
                
    return asteroids

def get_angle(base, asteroid):
    x = base.x - asteroid.x
    y = base.y - asteroid.y
    return math.atan2(x, y)

def count_seen_asteroids(base, asteroids):
    return len(set(get_angle(base, a) for a in asteroids if a != base))

def get_best_base(asteroids):
    possible_bases = ((a, count_seen_asteroids(a, asteroids)) for a in asteroids)
    return max(possible_bases, key=lambda x: x[1])

class Test(unittest.TestCase):
    def test_count_seen_asteroids(self):
        asteroids = read_file('test1.txt')
        def run_test(base_row, base_col, exp_count):
            base = Position(base_row, base_col)
            self.assertEqual(count_seen_asteroids(base, asteroids), exp_count)
        run_test(1, 0, 7)
        run_test(4, 0, 7)
        run_test(0, 2, 6)
        run_test(1, 2, 7)
        run_test(2, 2, 7)
        run_test(3, 2, 7)
        run_test(4, 2, 5)
        run_test(4, 3, 7)
        run_test(3, 4, 8)
        run_test(4, 4, 7)

    def test_get_best_base(self):
        def run_test(filename, exp):
            asteroids = read_file(filename)
            self.assertEqual(get_best_base(asteroids), exp)
        run_test('test1.txt', ((3,4), 8))
        run_test('test2.txt', ((5,8), 33))
        run_test('test3.txt', ((1,2), 35))
        run_test('test4.txt', ((6,3), 41))
        run_test('test5.txt', ((11,13), 210))

if __name__ == '__main__':
    unittest.main(exit=False)

    print(get_best_base(read_file('input.txt')))

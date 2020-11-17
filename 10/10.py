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
    y = base.y - asteroid.y # +y is towards y = 0
    x = asteroid.x - base.x # +x is towards right
    return math.atan2(y, x)

def normalize_angle(angle):
    # Reverse rotation to go clockwise.
    angle *= -1
    # Shift so min is pointing up.
    angle += math.pi / 2
    # Push back to interval [0, 2pi]
    angle = angle % (2 * math.pi)
    return angle

def get_distance(base, asteroid):
    return abs(base.x - asteroid.x) + abs(base.y - asteroid.y)

def get_asteroid_angles(base, asteroids):
    angles = {}
    for asteroid in asteroids:
        if asteroid == base: continue
        angle = get_angle(base, asteroid)
        if angle not in angles:
            angles[angle] = []
        angles[angle].append(asteroid)
    for angle in angles:
        angles[angle].sort(key=lambda x: get_distance(base, x))
    return angles

def count_seen_asteroids(base, asteroids):
    return len(get_asteroid_angles(base, asteroids))

def get_best_base(asteroids):
    possible_bases = ((a, count_seen_asteroids(a, asteroids)) for a in asteroids)
    return max(possible_bases, key=lambda x: x[1])

def vaporize_asteroids(base, asteroids):
    angles = get_asteroid_angles(base, asteroids)
    vaporized_asteroids = []
    while angles:
        for angle in sorted(angles, key=normalize_angle):
            asteroid = angles[angle].pop(0)
            vaporized_asteroids.append(asteroid)
        # Remove angles that have no more asteroids
        for angle in [a for a in angles if not angles[a]]:
            del angles[angle]
    return vaporized_asteroids

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

    def test_vaporize_asteroids(self):
        asteroids = read_file('test5.txt')
        vaporized_asteroids = vaporize_asteroids(Position(11, 13), asteroids)
        self.assertEqual(len(vaporized_asteroids), 299)
        def run_test(num, x, y):
            self.assertEqual(vaporized_asteroids[num-1], Position(x, y))
        run_test(1, 11, 12)
        run_test(2, 12, 1)
        run_test(3, 12, 2)
        run_test(10, 12, 8)
        run_test(20, 16, 0)
        run_test(50, 16, 9)
        run_test(100, 10, 16)
        run_test(199, 9, 6)
        run_test(200, 8, 2)
        run_test(201, 10, 9)
        run_test(299, 11, 1)

if __name__ == '__main__':
    unittest.main(exit=False)

    asteroids = read_file('input.txt')
    base, _ = get_best_base(asteroids)
    vaporized_asteroids = vaporize_asteroids(base, asteroids)
    print(vaporized_asteroids[199])

#!/usr/bin/env python3

import copy
import itertools
import math
import re
import unittest
from collections import namedtuple

class Moon:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return f'pos={self.position}, vel={self.velocity}'

    def __eq__(self, other):
        if not isinstance(other, Moon):
            return NotImplemented
        return self.position == other.position and self.velocity == other.velocity

def apply_gravity(moons):
    for a, b in itertools.combinations(moons, 2):
        for dim in range(len(a.position)):
            if a.position[dim] > b.position[dim]:
                a.velocity[dim] -= 1
                b.velocity[dim] += 1
            elif a.position[dim] < b.position[dim]:
                a.velocity[dim] += 1
                b.velocity[dim] -= 1

def apply_velocity(moons):
    for moon in moons:
        for dim in range(len(moon.position)):
            moon.position[dim] += moon.velocity[dim]

def get_energy(moon):
    potential = sum(map(abs, moon.position))
    kinetic = sum(map(abs, moon.velocity))
    return potential * kinetic

def get_total_energy(moons):
    return sum(map(get_energy, moons))

def step(moons):
    apply_gravity(moons)
    apply_velocity(moons)

def is_repeated(moons, orig_moons, dim):
    return all(moons[i].position[dim] == orig_moons[i].position[dim] and moons[i].velocity[dim] == orig_moons[i].velocity[dim] for i in range(len(moons)))

def get_periods(moons):
    orig_moons = copy.deepcopy(moons)
    periods = [None, None, None]
    step_num = 0
    while not(all(periods)):
        step(moons)
        step_num += 1
        repeated = [is_repeated(moons, orig_moons, dim) for dim in range(3)]
        for dim, rep in enumerate(repeated):
            if rep and periods[dim] is None:
                periods[dim] = step_num
    return periods

def lcm(a, b):
    return a * b // math.gcd(a, b)

def get_global_period(moons):
    periods = get_periods(moons)
    return lcm(lcm(periods[0], periods[1]), periods[2])

def read_input(f):
    moons = []
    for line in f:
        matches = re.findall('-?[-0-9]+', line)
        assert(len(matches) == 3)
        position = [int(matches[0]), int(matches[1]), int(matches[2])]
        velocity = [0, 0, 0]
        moons.append(Moon(position, velocity))
    return moons

class Test(unittest.TestCase):
    def test_part1(self):
        with open('test1.txt') as f:
            moons = read_input(f)
        for _ in range(10):
            step(moons)
        self.assertEqual(len(moons), 4)
        self.assertEqual(moons[0], Moon([2, 1, -3], [-3, -2, 1]))
        self.assertEqual(moons[1], Moon([1, -8, 0], [-1, 1, 3]))
        self.assertEqual(moons[2], Moon([3, -6, 1], [3, 2, -3]))
        self.assertEqual(moons[3], Moon([2, 0, 4], [1, -1, -1]))
        self.assertEqual(get_total_energy(moons), 179)

        with open('test2.txt') as f:
            moons = read_input(f)
        for _ in range(100):
            step(moons)
        self.assertEqual(len(moons), 4)
        self.assertEqual(moons[0], Moon([8, -12, -9], [-7, 3, 0]))
        self.assertEqual(moons[1], Moon([13, 16, -3], [3, -11, -5]))
        self.assertEqual(moons[2], Moon([-29, -11, -1], [-3, 7, 4]))
        self.assertEqual(moons[3], Moon([16, -13, 23], [7, 1, 1]))
        self.assertEqual(get_total_energy(moons), 1940)

    def test_part2(self):
        with open('test1.txt') as f:
            moons = read_input(f)
        self.assertEqual(get_global_period(moons), 2772)

        with open('test2.txt') as f:
            moons = read_input(f)
        self.assertEqual(get_global_period(moons), 4686774924)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        moons = read_input(f)
    print(get_global_period(moons))

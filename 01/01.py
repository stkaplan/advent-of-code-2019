#!/usr/bin/env python3

import unittest

def calculate_fuel_part1(mass):
    return mass // 3 - 2

def calculate_fuel_part2(mass):
    total_fuel = 0
    fuel = mass
    while True:
        fuel = calculate_fuel_part1(fuel)
        if fuel <= 0:
            break
        total_fuel += fuel
    return total_fuel


total = 0
with open('input.txt') as f:
    for line in f:
        mass = int(line.rstrip())
        total += calculate_fuel_part2(mass)

class CalculateFuelTest(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(calculate_fuel_part1(12), 2)
        self.assertEqual(calculate_fuel_part1(14), 2)
        self.assertEqual(calculate_fuel_part1(1969), 654)
        self.assertEqual(calculate_fuel_part1(100756), 33583)

    def test_part2(self):
        self.assertEqual(calculate_fuel_part2(14), 2)
        self.assertEqual(calculate_fuel_part2(1969), 966)
        self.assertEqual(calculate_fuel_part2(100756), 50346)

if __name__ == '__main__':
    unittest.main(exit=False)
    print(total)

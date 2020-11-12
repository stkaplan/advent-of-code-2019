#!/usr/bin/env python3

import unittest

def parse_orbits(f):
    orbits = []
    for line in f:
        elements = line.rstrip().split(')')
        assert(len(elements) == 2)
        orbits.append((elements[0], elements[1]))
    return orbits

def add_children(orbit_map, unplaced_orbits, parent):
    if parent not in unplaced_orbits: # nothing orbits this body
        return

    assert(parent not in orbit_map)
    orbit_map[parent] = unplaced_orbits[parent]
    del unplaced_orbits[parent]
    for child in orbit_map[parent]:
        add_children(orbit_map, unplaced_orbits, child)

def get_orbit_map(orbits, root):
    unplaced_orbits = {}
    orbit_map = {}

    for parent, child in orbits:
        if parent not in unplaced_orbits:
            unplaced_orbits[parent] = []
        unplaced_orbits[parent].append(child)

    add_children(orbit_map, unplaced_orbits, root)

    return orbit_map

def get_total_orbits_inner(orbit_map, root, depth):
    if root not in orbit_map:
        return depth
    else:
        total = depth
        for child in orbit_map[root]:
            total += get_total_orbits_inner(orbit_map, child, depth+1)
        return total

def get_total_orbits(orbits):
    root = 'COM'
    orbit_map = get_orbit_map(orbits, root)
    return get_total_orbits_inner(orbit_map, root, 0)

class RunProgramTest(unittest.TestCase):
    def test_part1(self):
        orbits = parse_orbits(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L'])
        self.assertEqual(get_total_orbits(orbits), 42)

        with open('input.txt') as f:
            orbits = parse_orbits(f)
        self.assertEqual(get_total_orbits(orbits), 308790)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        orbits = parse_orbits(f)

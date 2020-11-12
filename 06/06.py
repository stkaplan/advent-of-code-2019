#!/usr/bin/env python3

import unittest

def parse_orbits(f):
    orbits = []
    for line in f:
        elements = line.rstrip().split(')')
        assert(len(elements) == 2)
        orbits.append((elements[0], elements[1]))
    return orbits

def add_orbit(orbit_distances, unplaced_orbits, orbit):
    (parent, child) = orbit
    if parent == 'COM':
        orbit_distances[parent] = 0
        orbit_distances[child] = 1
    elif parent in orbit_distances:
        orbit_distances[child] = orbit_distances[parent] + 1
    else:
        if parent not in unplaced_orbits:
            unplaced_orbits[parent] = []
        unplaced_orbits[parent].append(child)

def get_orbit_distances(orbits):
    unplaced_orbits = {} # map of parent to list of orbiting children
    orbit_distances = {} # map of body to distance from COM

    for orbit in orbits:
        add_orbit(orbit_distances, unplaced_orbits, orbit)

    while len(unplaced_orbits) > 0:
        new_orbit_distances = {}
        for body in orbit_distances:
            children = unplaced_orbits.pop(body, [])
            for child in children:
                new_orbit_distances[child] = orbit_distances[body] + 1

        orbit_distances.update(new_orbit_distances)

    return orbit_distances

def get_total_orbits(orbits):
    orbit_distances = get_orbit_distances(orbits)
    return sum(orbit_distances.values())

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

    print(get_total_orbits(orbits))

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

def get_parent_map(orbits):
    parent_map = {}
    for parent, child in orbits:
        assert child not in parent_map
        parent_map[child] = parent
    return parent_map

def get_parents(parent_map, body):
    if body in parent_map:
        parent = parent_map[body]
        return [parent] + get_parents(parent_map, parent)
    else:
        assert(body == 'COM')
        return []

def get_total_orbits_inner(orbit_map, root, depth):
    if root not in orbit_map:
        return depth
    else:
        total = depth
        for child in orbit_map[root]:
            total += get_total_orbits_inner(orbit_map, child, depth+1)
        return total

def get_total_orbits(orbits):
    orbit_map = get_orbit_map(orbits, 'COM')
    return get_total_orbits_inner(orbit_map, 'COM', 0)

def is_child(orbit_map, root, target):
    if root not in orbit_map:
        return False
    elif target in orbit_map[root]:
        return True
    else:
        return any(is_child(orbit_map, child, target) for child in orbit_map[root])

def get_first_common_parent_indexes(src_parents, dst_parents):
    for i, src_parent in enumerate(src_parents):
        for j, dst_parent in enumerate(dst_parents):
            if src_parent == dst_parent:
                return (i, j)
    return None

# NOTE: Doesn't consider the case where you only have to move "in" or "out",
# i.e. src is a (direct or indirect) parent of dst, or vice versa.
def get_shortest_travel_distance(orbits, src, dst):
    parent_map = get_parent_map(orbits)
    src_parents = get_parents(parent_map, src)
    dst_parents = get_parents(parent_map, dst)
    (i, j) = get_first_common_parent_indexes(src_parents, dst_parents)
    return i + j

class Test(unittest.TestCase):
    small_test_case = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']

    def test_get_total_orbits(self):
        orbits = parse_orbits(Test.small_test_case)
        self.assertEqual(get_total_orbits(orbits), 42)

        with open('input.txt') as f:
            orbits = parse_orbits(f)
        self.assertEqual(get_total_orbits(orbits), 308790)

    def test_get_shortest_travel_distance(self):
        orbits = parse_orbits(Test.small_test_case + ['K)YOU', 'I)SAN'])
        self.assertEqual(get_shortest_travel_distance(orbits, 'YOU', 'SAN'), 4)

        with open('input.txt') as f:
            orbits = parse_orbits(f)
        self.assertEqual(get_shortest_travel_distance(orbits, 'YOU', 'SAN'), 472)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        orbits = parse_orbits(f)

    print(get_shortest_travel_distance(orbits, 'YOU', 'SAN'))

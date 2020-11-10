#!/usr/bin/env python3

import unittest
from collections import namedtuple

Step = namedtuple('Step', ['direction', 'distance'])
Position = namedtuple('Position', ['x', 'y'])

def parse_input(lines):
    return list(map(parse_line, lines))

def parse_line(line):
    return [Step(x[0], int(x[1:])) for x in line.split(',')]

def trace_path(path):
    points = {}
    steps = 0
    position = Position(0, 0)
    for step in path:
        for _ in range(step.distance):
            steps += 1
            if step.direction == 'U':
                position = Position(position.x, position.y + 1)
            elif step.direction == 'D':
                position = Position(position.x, position.y - 1)
            elif step.direction == 'L':
                position = Position(position.x - 1, position.y)
            elif step.direction == 'R':
                position = Position(position.x + 1, position.y)

            if position not in points:
                points[position] = steps

    return points

def find_intersections(path1, path2):
    points1 = trace_path(path1)
    points2 = trace_path(path2)
    return {x: points1[x] + points2[x] for x in points1 if x in points2}

def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def find_smallest_distance(points):
    return min([manhattan_distance(point, Position(0, 0)) for point in points])

def part1(lines):
    paths = parse_input(lines)
    return find_smallest_distance(find_intersections(paths[0], paths[1]))
        
def part2(lines):
    paths = parse_input(lines)
    return min(find_intersections(paths[0], paths[1]).values())

class RunProgramTest(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1([
            'R75,D30,R83,U83,L12,D49,R71,U7,L72',
            'U62,R66,U55,R34,D71,R55,D58,R83',
        ]), 159)
        self.assertEqual(part1([
            'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
        ]), 135)

    def test_part2(self):
        self.assertEqual(part2([
            'R75,D30,R83,U83,L12,D49,R71,U7,L72',
            'U62,R66,U55,R34,D71,R55,D58,R83',
        ]), 610)
        self.assertEqual(part2([
            'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
        ]), 410)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        #print(part1(f.readlines()))
        print(part2(f.readlines()))

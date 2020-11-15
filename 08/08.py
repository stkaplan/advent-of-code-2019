#!/usr/bin/env python3

import io
import unittest

def read_input(f, width, height):
    layers = []
    while True:
        layer = f.read(width * height).rstrip()
        if not layer:
            break
        layers.append(list(map(int, layer)))
    return layers

def get_num_zeroes(layer):
    return layer.count(0)

def get_layer_with_most_zeroes(layers):
    return max(range(len(layers)), key=layers.__getitem__)

class Test(unittest.TestCase):
    def test_read_input(self):
        data = io.StringIO('123456789012')
        layers = read_input(data, 3, 2)
        self.assertEqual(layers, [[1,2,3,4,5,6], [7,8,9,0,1,2]])

    def test_get_layer_with_most_zeroes(self):
        data = io.StringIO('123456789012')
        layers = read_input(data, 3, 2)
        self.assertEqual(get_layer_with_most_zeroes(layers), 1)

        with open('input.txt') as f:
            layers = read_input(f, 25, 6)
            self.assertEqual(get_layer_with_most_zeroes(layers), 13)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        layers = read_input(f, 25, 6)

    index = get_layer_with_most_zeroes(layers)
    print(layers[index].count(1) * layers[index].count(2))

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

def stack_layers(layers):
    black = 0
    white = 1
    transparent = 2

    image = []
    assert(all(len(layer) == len(layers[0]) for layer in layers))
    for i in range(len(layers[0])):
        pixel = next((layer[i] for layer in layers if layer[i] != transparent), black)
        image.append(pixel)
    return image

def print_image(image, width, height):
    assert(len(image) == width * height)
    for row in range(height):
        for col in range(width):
            print('*' if image[row*width + col] else ' ', end='')
        print()

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

    def test_stack_layers(self):
        data = io.StringIO('0222112222120000')
        layers = read_input(data, 2, 2)
        image = stack_layers(layers)
        self.assertEqual(image, [0,1,1,0])

if __name__ == '__main__':
    unittest.main(exit=False)

    width = 25
    height = 6
    with open('input.txt') as f:
        layers = read_input(f, width, height)

    index = get_layer_with_most_zeroes(layers)
    print(layers[index].count(1) * layers[index].count(2))

    image = stack_layers(layers)
    print_image(image, width, height)

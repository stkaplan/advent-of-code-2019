#!/usr/bin/env python3

import itertools
import unittest
from collections import namedtuple
from enum import IntEnum

class ParameterMode(IntEnum):
    position = 0
    immediate = 1
    relative = 2
    relative_output = 3

def read_input():
    with open('input.txt') as f:
        mem = list(map(int, f.read().split(',')))
    return mem

def print_mem(mem):
    print(','.join(map(str, mem)))

class Program:
    def __init__(self, mem, input_=None):
        self.mem = mem
        self.pc = 0
        self.input = input_ if input_ else []
        self.input_offset = 0
        self.output = []
        self.relative_base = 0

    def run(self):
        while self.pc is not None:
            self.pc = self.run_instruction()

    def get_next_output(self):
        initial_output_len = len(self.output)
        while self.pc is not None and len(self.output) == initial_output_len:
            self.pc = self.run_instruction()
        if self.pc is None:
            return None
        else:
            return self.output[-1]

    def pad_mem(self, new_len):
        if new_len > len(self.mem):
            self.mem += [0] * (new_len - len(self.mem))

    def get_mem(self, addr):
        self.pad_mem(addr+1)
        return self.mem[addr]

    def set_mem(self, addr, val):
        self.pad_mem(addr+1)
        self.mem[addr] = val

    @staticmethod
    def parse_opcode(val):
        val, opcode = divmod(val, 100)
        modes = []
        while val > 0:
            val, mode = divmod(val, 10)
            modes.append(mode)
        return (opcode, modes)

    def get_parameter_value(self, i, modes):
        loc = self.pc + i + 1
        if modes[i] == ParameterMode.position:
            return self.get_mem(self.get_mem(loc))
        elif modes[i] == ParameterMode.immediate:
            return self.get_mem(loc)
        elif modes[i] == ParameterMode.relative:
            return self.get_mem(self.get_mem(loc) + self.relative_base)
        elif modes[i] == ParameterMode.relative_output:
            return self.get_mem(loc) + self.relative_base
        else:
            raise Exception(f'Invalid parameter mode: {modes[i]}')

    # Generic decorator to set up params, based on parameter modes
    def opcode_template(num_params, output_params):
        def decorator(func):
            def inner(self, modes):
                modes += [ParameterMode.position] * (num_params - len(modes))
                for i in output_params:
                    # Output paramters are not actually immediate mode, but we want
                    # to treat them as such: they return the output location, not
                    # the value at the output location.
                    if modes[i] == ParameterMode.position:
                        modes[i] = ParameterMode.immediate
                    elif modes[i] == ParameterMode.relative:
                        modes[i] = ParameterMode.relative_output
                params = [self.get_parameter_value(i, modes) for i in range(0, num_params)]
                return func(self, params)
            return inner
        return decorator

    @opcode_template(3, [2])
    def opcode_add(self, params):
        self.set_mem(params[2], params[0] + params[1])
        return self.pc + len(params) + 1

    @opcode_template(3, [2])
    def opcode_multiply(self, params):
        self.set_mem(params[2], params[0] * params[1])
        return self.pc + len(params) + 1

    @opcode_template(1, [0])
    def opcode_input(self, params):
        self.set_mem(params[0], self.input[self.input_offset])
        self.input_offset += 1
        return self.pc + len(params) + 1

    @opcode_template(1, [])
    def opcode_output(self, params):
        self.output.append(params[0])
        return self.pc + len(params) + 1

    @opcode_template(2, [])
    def opcode_jump_if_true(self, params):
        return params[1] if params[0] != 0 else self.pc + len(params) + 1

    @opcode_template(2, [])
    def opcode_jump_if_false(self, params):
        return params[1] if params[0] == 0 else self.pc + len(params) + 1

    @opcode_template(3, [2])
    def opcode_less_than(self, params):
        self.set_mem(params[2], int(params[0] < params[1]))
        return self.pc + len(params) + 1

    @opcode_template(3, [2])
    def opcode_equals(self, params):
        self.set_mem(params[2], int(params[0] == params[1]))
        return self.pc + len(params) + 1

    @opcode_template(1, [])
    def opcode_adjust_relative_base(self, params):
        self.relative_base += params[0]
        return self.pc + len(params) + 1

    @opcode_template(0, [])
    def opcode_exit(self, modes):
        return None

    # Returns PC of next instruction, or None if program should exit
    def run_instruction(self):
        opcodes = {
            1: self.opcode_add,
            2: self.opcode_multiply,
            3: self.opcode_input,
            4: self.opcode_output,
            5: self.opcode_jump_if_true,
            6: self.opcode_jump_if_false,
            7: self.opcode_less_than,
            8: self.opcode_equals,
            9: self.opcode_adjust_relative_base,
            99: self.opcode_exit,
        }

        (opcode, modes) = self.parse_opcode(self.mem[self.pc])
        if opcode not in opcodes:
            raise Exception(f'Invalid opcode: {opcode}')
        return opcodes[opcode](modes)

class TileType(IntEnum):
    empty = 0
    wall = 1
    block = 2
    paddle = 3
    ball = 4

Position = namedtuple('Position', ['x', 'y'])
TilePosition = namedtuple('TilePosition', ['x', 'y', 'type'])

class Game:
    def __init__(self, mem):
        self.score = 0
        self.program = Program(mem)
        self.tiles = {}

    def get_next_tile(self):
        x = self.program.get_next_output()
        if x is None:
            return None
        y = self.program.get_next_output()
        assert(y is not None)
        tile = self.program.get_next_output()
        assert(tile is not None)
        return TilePosition(x, y, tile)

    def move_joystick(self):
        ball_position = [pos for pos, tile in self.tiles.items() if tile == TileType.ball]
        paddle_position = [pos for pos, tile in self.tiles.items() if tile == TileType.paddle]
        if not ball_position or not paddle_position:
            return

        assert(len(ball_position) == 1)
        assert(len(paddle_position) == 1)
        if paddle_position[0].x < ball_position[0].x:
            input_ = 1
        elif paddle_position[0].x > ball_position[0].x:
            input_ = -1
        else:
            input_ = 0

        # Don't append to the input list, since this might not be the next
        # input read. Instead overwrite the input list entirely.
        self.program.input = [input_]
        self.program.input_offset = 0

    def run_game(self):
        while True:
            tile = self.get_next_tile()
            if tile is None:
                break
            elif tile.x == -1 and tile.y == 0:
                self.score = tile.type
            else:
                self.tiles[Position(tile.x, tile.y)] = tile.type

            self.move_joystick()

    def count_blocks(self):
        return sum(tile_type == TileType.block for tile_type in self.tiles.values())

class Test(unittest.TestCase):
    def run_test(self, mem, output_mem, input_='', output=''):
        program = Program(mem, input_)
        program.run()
        if output_mem is not None:
            self.assertEqual(program.mem, output_mem)
        if output:
            self.assertEqual(program.output, output)

    def test_run_program(self):
        self.run_test([1,0,0,0,99], [2,0,0,0,99])
        self.run_test([2,3,0,3,99], [2,3,0,6,99])
        self.run_test([2,4,4,5,99,0], [2,4,4,5,99,9801])
        self.run_test([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
        self.run_test([1101,100,-1,4,0], [1101,100,-1,4,99])
        self.run_test([1001,5,-1,4,0,100], [1001,5,-1,4,99,100])
        self.run_test([3,9,8,9,10,9,4,9,99,-1,8], None, [8], [1])
        self.run_test([3,9,8,9,10,9,4,9,99,-1,8], None, [1], [0])
        self.run_test([3,9,8,9,10,9,4,9,99,-1,8], None, [9], [0])
        self.run_test([3,9,7,9,10,9,4,9,99,-1,8], None, [-1], [1])
        self.run_test([3,9,7,9,10,9,4,9,99,-1,8], None, [8], [0])
        self.run_test([3,9,7,9,10,9,4,9,99,-1,8], None, [9], [0])
        self.run_test([3,3,1108,-1,8,3,4,3,99], None, [8], [1])
        self.run_test([3,3,1108,-1,8,3,4,3,99], None, [1], [0])
        self.run_test([3,3,1108,-1,8,3,4,3,99], None, [9], [0])
        self.run_test([3,3,1107,-1,8,3,4,3,99], None, [-1], [1])
        self.run_test([3,3,1107,-1,8,3,4,3,99], None, [8], [0])
        self.run_test([3,3,1107,-1,8,3,4,3,99], None, [9], [0])
        self.run_test([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], None, [0], [0])
        self.run_test([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], None, [5], [1])
        self.run_test([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], None, [0], [0])
        self.run_test([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], None, [5], [1])
        self.run_test([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], None, [3], [999])
        self.run_test([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], None, [8], [1000])
        self.run_test([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], None, [10], [1001])

        quine = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        self.run_test([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], None, [], quine)

        self.run_test([1102,34915192,34915192,7,4,7,99,0], None, [], [1219070632396864])
        self.run_test([104,1125899906842624,99], None, [], [1125899906842624])

    def test_run_game(self):
        mem = read_input()
        game = Game(mem)
        game.run_game()
        self.assertEqual(game.count_blocks(), 414)

if __name__ == '__main__':
    unittest.main(exit=False)

    mem = read_input()
    mem[0] = 2 # Insert coins
    game = Game(mem)
    game.run_game()
    assert(game.count_blocks() == 0)
    print(game.score)

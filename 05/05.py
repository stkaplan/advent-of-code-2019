#!/usr/bin/env python3

import unittest

def read_input():
    with open('input.txt') as f:
        mem = list(map(int, f.read().split(',')))
    return mem

def print_mem(mem):
    print(','.join(map(str, mem)))

class Program:
    def __init__(self, mem, input_=''):
        self.mem = mem
        self.pc = 0
        self.input = input_
        self.output = ''

    def run(self):
        self.pc = 0
        while True:
            self.pc = self.run_instruction()
            if self.pc is None:
                break

    @staticmethod
    def parse_opcode(val):
        val, opcode = divmod(val, 100)
        modes = []
        while val > 0:
            val, mode = divmod(val, 10)
            assert(mode in [0,1])
            modes.append(bool(mode))
        return (opcode, modes)

    def get_parameter_value(self, i, modes):
        return self.mem[self.pc+i+1] if modes[i] else self.mem[self.mem[self.pc+i+1]]

    # Generic decorator to set up params, based on parameter modes
    def opcode_template(num_params, output_params):
        def decorator(func):
            def inner(self, modes):
                modes += [False] * (num_params - len(modes))
                for i in output_params:
                    # Output paramters are not actually immediate mode, but we want
                    # to treat them as such: they return the output location, not
                    # the value at the output location.
                    modes[i] = True
                params = [self.get_parameter_value(i, modes) for i in range(0, num_params)]
                return func(self, params)
            return inner
        return decorator

    @opcode_template(3, [2])
    def opcode_add(self, params):
        self.mem[params[2]] = params[0] + params[1]
        return self.pc + len(params) + 1

    @opcode_template(3, [2])
    def opcode_multiply(self, params):
        self.mem[params[2]] = params[0] * params[1]
        return self.pc + len(params) + 1

    @opcode_template(1, [0])
    def opcode_input(self, params):
        input_str = input()
        input_val = int(input_str.rstrip())
        self.mem[params[0]] = input_val
        return self.pc + len(params) + 1

    @opcode_template(1, [])
    def opcode_output(self, params):
        print(params[0])
        return self.pc + len(params) + 1

    @opcode_template(2, [])
    def opcode_jump_if_true(self, params):
        return params[1] if params[0] != 0 else self.pc + len(params) + 1

    @opcode_template(2, [])
    def opcode_jump_if_false(self, params):
        return params[1] if params[0] == 0 else self.pc + len(params) + 1

    @opcode_template(3, [2])
    def opcode_less_than(self, params):
        self.mem[params[2]] = int(params[0] < params[1])
        return self.pc + len(params) + 1

    @opcode_template(3, [2])
    def opcode_equals(self, params):
        self.mem[params[2]] = int(params[0] == params[1])
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
            99: self.opcode_exit,
        }

        (opcode, modes) = self.parse_opcode(self.mem[self.pc])
        if opcode not in opcodes:
            raise Exception(f'Invalid opcode: {opcode}')
        return opcodes[opcode](modes)

class RunProgramTest(unittest.TestCase):
    def run_test(self, mem, output_mem, input_='', output=''):
        program = Program(mem, input_)
        program.run()
        if output_mem is not None:
            self.assertEqual(mem, output_mem)

    def test_run_program(self):
        self.run_test([1,0,0,0,99], [2,0,0,0,99])
        self.run_test([2,3,0,3,99], [2,3,0,6,99])
        self.run_test([2,4,4,5,99,0], [2,4,4,5,99,9801])
        self.run_test([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
        self.run_test([1101,100,-1,4,0], [1101,100,-1,4,99])
        self.run_test([1001,5,-1,4,0,100], [1001,5,-1,4,99,100])

if __name__ == '__main__':
    unittest.main(exit=False)

    mem = read_input()
    program = Program(mem)
    program.run()

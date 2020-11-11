#!/usr/bin/env python3

import unittest

def read_input():
    with open('input.txt') as f:
        mem = list(map(int, f.read().split(',')))
    return mem

def print_mem(mem):
    print(','.join(map(str, mem)))

def run_program(mem):
    pc = 0
    while True:
        pc = run_instruction(mem, pc)
        if pc is None:
            break

def parse_opcode(val):
    val, opcode = divmod(val, 100)
    modes = []
    while val > 0:
        val, mode = divmod(val, 10)
        assert(mode in [0,1])
        modes.append(bool(mode))
    return (opcode, modes)

def get_parameter_value(mem, pc, i, modes):
    return mem[pc+i+1] if modes[i] else mem[mem[pc+i+1]]

# Generic decorator to set up params, based on parameter modes
def opcode_template(num_params, output_params):
    def decorator(func):
        def inner(mem, pc, modes):
            modes += [False] * (num_params - len(modes))
            for i in output_params:
                # Output paramters are not actually immediate mode, but we want
                # to treat them as such: they return the output location, not
                # the value at the output location.
                modes[i] = True
            params = [get_parameter_value(mem, pc, i, modes) for i in range(0, num_params)]
            return func(mem, pc, params)
        return inner
    return decorator

@opcode_template(3, [2])
def opcode_add(mem, pc, params):
    mem[params[2]] = params[0] + params[1]
    return pc + len(params) + 1

@opcode_template(3, [2])
def opcode_multiply(mem, pc, params):
    mem[params[2]] = params[0] * params[1]
    return pc + len(params) + 1

@opcode_template(1, [0])
def opcode_input(mem, pc, params):
    input_str = input()
    input_val = int(input_str.rstrip())
    mem[params[0]] = input_val
    return pc + len(params) + 1

@opcode_template(1, [])
def opcode_output(mem, pc, params):
    print(params[0])
    return pc + len(params) + 1

@opcode_template(2, [])
def opcode_jump_if_true(mem, pc, params):
    return params[1] if params[0] != 0 else pc + len(params) + 1

@opcode_template(2, [])
def opcode_jump_if_false(mem, pc, params):
    return params[1] if params[0] == 0 else pc + len(params) + 1

@opcode_template(3, [2])
def opcode_less_than(mem, pc, params):
    mem[params[2]] = int(params[0] < params[1])
    return pc + len(params) + 1

@opcode_template(3, [2])
def opcode_equals(mem, pc, params):
    mem[params[2]] = int(params[0] == params[1])
    return pc + len(params) + 1

@opcode_template(0, [])
def opcode_exit(mem, pc, modes):
    return None

# Returns PC of next instruction, or None if program should exit
def run_instruction(mem, pc):
    opcodes = {
        1: opcode_add,
        2: opcode_multiply,
        3: opcode_input,
        4: opcode_output,
        5: opcode_jump_if_true,
        6: opcode_jump_if_false,
        7: opcode_less_than,
        8: opcode_equals,
        99: opcode_exit,
    }

    (opcode, modes) = parse_opcode(mem[pc])
    if opcode not in opcodes:
        raise Exception(f'Invalid opcode: {opcode}')
    return opcodes[opcode](mem, pc, modes)

class RunProgramTest(unittest.TestCase):
    def run_test(self, input, output):
        run_program(input)
        self.assertEqual(input, output)

    def test_run_program(self):
        self.run_test([1,0,0,0,99], [2,0,0,0,99])
        self.run_test([2,3,0,3,99], [2,3,0,6,99])
        self.run_test([2,4,4,5,99,0], [2,4,4,5,99,9801])
        self.run_test([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
        self.run_test([1101,100,-1,4,0], [1101,100,-1,4,99])
        self.run_test([1001,5,-1,4,0,100], [1001,5,-1,4,99,100])

if __name__ == '__main__':
    unittest.main(exit=False)

    mem = [3,9,8,9,10,9,4,9,99,-1,8]
    #mem = read_input()
    run_program(mem)

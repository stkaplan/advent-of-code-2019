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

def is_immediate(modes, i):
    return i <= len(modes) and modes[i-1]

def get_parameter_value(mem, pc, i, modes):
    return mem[pc+i] if is_immediate(modes, i) else mem[mem[pc+i]]

def opcode_add(mem, pc, modes):
    val1 = get_parameter_value(mem, pc, 1, modes)
    val2 = get_parameter_value(mem, pc, 2, modes)
    mem[mem[pc+3]] = val1 + val2
    return pc+4

def opcode_multiply(mem, pc, modes):
    val1 = get_parameter_value(mem, pc, 1, modes)
    val2 = get_parameter_value(mem, pc, 2, modes)
    mem[mem[pc+3]] = val1 * val2
    return pc+4

def opcode_input(mem, pc, modes):
    input_str = input('Enter a value: ')
    input_val = int(input_str.rstrip())
    mem[mem[pc+1]] = input_val
    return pc+2

def opcode_output(mem, pc, modes):
    print(get_parameter_value(mem, pc, 1, modes))
    return pc+2

def opcode_exit(mem, pc, modes):
    return None

# Returns PC of next instruction, or None if program should exit
def run_instruction(mem, pc):
    opcodes = {
        1: opcode_add,
        2: opcode_multiply,
        3: opcode_input,
        4: opcode_output,
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

    mem = read_input()
    run_program(mem)

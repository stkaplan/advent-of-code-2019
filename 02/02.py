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

def opcode_add(mem, pc):
    mem[mem[pc+3]] = mem[mem[pc+1]] + mem[mem[pc+2]]
    return pc+4

def opcode_multiply(mem, pc):
    mem[mem[pc+3]] = mem[mem[pc+1]] * mem[mem[pc+2]]
    return pc+4

def opcode_exit(mem, pc):
    return None

# Returns PC of next instruction, or None if program should exit
def run_instruction(mem, pc):
    opcodes = {
        1: opcode_add,
        2: opcode_multiply,
        99: opcode_exit,
    }

    opcode = mem[pc]
    if opcode not in opcodes:
        raise Exception(f'Invalid opcode: {opcode}')
    return opcodes[mem[pc]](mem, pc)

class RunProgramTest(unittest.TestCase):
    def run_test(self, input, output):
        run_program(input)
        self.assertEqual(input, output)

    def test_run_program(self):
        self.run_test([1,0,0,0,99], [2,0,0,0,99])
        self.run_test([2,3,0,3,99], [2,3,0,6,99])
        self.run_test([2,4,4,5,99,0], [2,4,4,5,99,9801])
        self.run_test([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])

if __name__ == '__main__':
    unittest.main(exit=False)

    mem = read_input()
    mem[1] = 12
    mem[2] = 2
    run_program(mem)
    print_mem(mem)

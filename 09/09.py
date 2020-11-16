#!/usr/bin/env python3

import itertools
import unittest

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
        self.mem[params[0]] = self.input[self.input_offset]
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

def create_amps(mem, perm):
    amps = []
    for i in range(len(perm)):
        amp = Program(mem.copy(), [perm[i]])
        amps.append(amp)
    return amps

def get_next_signal(amps, signal):
    for amp in amps:
        amp.input.append(signal)
        signal = amp.get_next_output()
    return signal

def get_final_signal(mem, perm):
    amps = create_amps(mem, perm)
    return get_next_signal(amps, 0)

def get_max_final_signal(mem):
    num_amplifiers = 5
    perms = itertools.permutations(range(num_amplifiers))
    return max(get_final_signal(mem, perm) for perm in perms)

def get_final_signal_with_feedback(mem, perm, initial_signal):
    amps = create_amps(mem, perm)
    signal = 0

    while True:
        new_signal = get_next_signal(amps, signal)
        if new_signal is None:
            return signal
        signal = new_signal

def get_max_final_signal_with_feedback(mem):
    num_amplifiers = 5
    perms = itertools.permutations(range(num_amplifiers, num_amplifiers*2))
    return max(get_final_signal_with_feedback(mem, perm, 0) for perm in perms)

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

    def test_get_max_final_signal(self):
        self.assertEqual(get_max_final_signal([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]), 43210)
        self.assertEqual(get_max_final_signal([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]), 54321)
        self.assertEqual(get_max_final_signal([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]), 65210)

        mem = read_input()
        self.assertEqual(get_max_final_signal(mem), 46248)

    def test_get_max_final_signal_with_feedback(self):
        self.assertEqual(get_max_final_signal_with_feedback([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]), 139629729)
        self.assertEqual(get_max_final_signal_with_feedback([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]), 18216)

        mem = read_input()
        self.assertEqual(get_max_final_signal_with_feedback(mem), 54163586)

if __name__ == '__main__':
    unittest.main(exit=False)

    mem = read_input()
    print(get_max_final_signal_with_feedback(mem))

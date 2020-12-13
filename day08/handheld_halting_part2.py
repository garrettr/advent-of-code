#!/usr/bin/env python3

from copy import deepcopy


class InvalidOperation(Exception):
    pass


class InvalidInstruction(Exception):
    def __init__(self, code, index):
        self.code = code
        self.index = index

    def __repr__(self):
        # Range notation: inclusive [x, y], exclusive [x, y)
        return f'{self.index} not in range [0, {len(self.code)})'


class InfiniteLoop(Exception):
    pass

    
class Instruction:
    def __init__(self, operation, argument):
        self.operation = operation
        self.argument = argument

    @classmethod
    def from_string(cls, s):
        operation, argument = s.split()[:2]
        return cls(operation, int(argument))

    def __repr__(self):
        return f'{self.operation} {self.argument}'


class Code:
    def __init__(self, instructions):
        self._instructions = instructions

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            return cls([Instruction.from_string(line) for line in f.readlines()])

    def __len__(self):
        return len(self._instructions)

    def __getitem__(self, position):
        return self._instructions[position]

    def __iter__(self):
        return (instruction for instruction in self._instructions)


class CodeCorrector:
    def __init__(self, code):
        self.code = code

    def __iter__(self):
        for i, instruction in enumerate(self.code):
            if instruction.operation in ('jmp', 'nop'):
                copy = deepcopy(self.code)
                copy[i].operation = 'jmp' if instruction.operation == 'nop' else 'nop'
                yield copy
            else:
                continue


class State:
    def __init__(self, acc=0, ip=0):
        self.acc = acc
        self.ip = ip

    def execute(self, instruction):
        acc = self.acc
        ip = self.ip
        
        if instruction.operation == 'acc':
            acc += instruction.argument
            ip += 1
        elif instruction.operation == 'jmp':
            ip += instruction.argument
        elif instruction.operation == 'nop':
            ip += 1
        else:
            raise InvalidOperation(instruction.operation)

        return State(acc, ip)

    def __repr__(self):
        return f'ip={self.ip} acc={self.acc}'


class Interpreter:
    def __init__(self, code):
        self.code = code
        self.state = State()
        self.terminated = False
        self.ips = set()

    def _detect_infinite_loop(self):
        if self.state.ip in self.ips:
            raise InfiniteLoop

        self.ips.add(self.state.ip)

    def next(self):
        self._detect_infinite_loop()

        try:
            instruction = self.code[self.state.ip]
        except IndexError as exception:
            raise InvalidInstruction(self.code, self.state.ip) from exception

        self.state = self.state.execute(instruction)

        if self.state.ip == len(self.code):
            self.terminated = True

    def run(self):
        while not self.terminated:
            try:
                self.next()
            except InfiniteLoop:
                return None

        return self.state


def main():
    code = Code.from_file('input.txt')
    code_corrector = CodeCorrector(code)

    for corrected_code in code_corrector:
        interpreter = Interpreter(corrected_code)
        result = interpreter.run()
        if result:
            print(f'{result.acc}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

class InvalidOperation(Exception):
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
    

class Interpreter:
    def __init__(self, code):
        self.code = code
        self.state = State()
        
    def next(self):
        instruction = self.code[self.state.ip]
        prior_state = self.state
        self.state = self.state.execute(instruction)
        return (prior_state, self.state)


def main():
    code = Code.from_file('input.txt')
    interpreter = Interpreter(code)
    
    ips = set()
    while interpreter.state.ip not in ips:
        ips.add(interpreter.state.ip)
        interpreter.next()

    print(f'{interpreter.state.acc}')


if __name__ == '__main__':
    main()

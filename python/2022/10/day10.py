#!/usr/bin/env python3
import os

TINY_TEST = """noop
addx 3
addx -5"""


def parse(string):
    return [line.split() for line in string.splitlines()]


def execute(instructions):
    X = 1
    cycle = 1
    signal_strengths = {}
    ip = 0

    for instruction in instructions:
        op = instruction[0]

        if op == "noop":
            run_for = 1
        elif op == "addx":
            run_for = 2

        for i in range(run_for):
            if cycle % 40 == 20:
                signal_strengths[cycle] = cycle * X
            cycle += 1

        if op == "noop":
            pass
        elif op == "addx":
            X += int(instruction[1])

    return signal_strengths


def part1(instructions):
    signal_strengths = execute(instructions)
    return sum(signal_strengths[i] for i in range(20, 220 + 1, 40))


# instructions = parse(TINY_TEST)
# input_filename = "test.txt"
input_filename = "input.txt"
input_path = os.path.join(os.path.dirname(__file__), input_filename)
with open(input_path) as f:
    instructions = parse(f.read())
print(part1(instructions))

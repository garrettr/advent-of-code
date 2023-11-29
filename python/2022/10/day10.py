#!/usr/bin/env python3
from advent import get_puzzle_input

TINY_TEST = """noop
addx 3
addx -5"""


def parse_instructions(string: str) -> list[list[str]]:
    return [line.split() for line in string.splitlines()]


class CPU:
    def __init__(self):
        self.X = 1
        self.cycle = 1
        self.signal_strengths = {}
        self.CRT = [[" "] * 40 for _ in range(6)]

    def update_signal_strengths(self):
        if self.cycle % 40 == 20:
            self.signal_strengths[self.cycle] = self.cycle * self.X

    def current_pixel(self):
        return ((self.cycle - 1) % 40, (self.cycle - 1) // 40)

    def update_CRT(self):
        x, y = self.current_pixel()
        self.CRT[y][x] = (
            "#" if self.X in (x + offset for offset in range(-1, 2)) else "."
        )

    def execute(self, instructions):
        ip = 0

        for instruction in instructions:
            op = instruction[0]

            if op == "noop":
                run_for = 1
            elif op == "addx":
                run_for = 2

            for i in range(run_for):
                self.update_signal_strengths()
                self.update_CRT()
                self.cycle += 1

            if op == "noop":
                pass
            elif op == "addx":
                self.X += int(instruction[1])

    def CRT_as_str(self):
        return "\n".join("".join(row) for row in self.CRT)


def part1(instructions):
    cpu = CPU()
    cpu.execute(instructions)
    return sum(cpu.signal_strengths[i] for i in range(20, 220 + 1, 40))


def part2(instructions):
    cpu = CPU()
    cpu.execute(instructions)
    return cpu.CRT_as_str()


instructions = parse_instructions(get_puzzle_input(2022, 10))
print(part1(instructions))
print(part2(instructions))

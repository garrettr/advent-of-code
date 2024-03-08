#!/usr/bin/env python3
from collections import defaultdict
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 2
EXAMPLE = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def parse(input: str) -> dict[str, int]:
    commands = defaultdict(int)
    for line in input.strip().split("\n"):
        action, value = line.split()
        commands[action] += int(value)
    return commands


def part1(input: str):
    commands = parse(input)
    horizontal_position = commands["forward"]
    depth = commands["down"] - commands["up"]
    return horizontal_position * depth


def part2(input: str):
    pass


class TestDay2(unittest.TestCase):
    def setUp(self):
        self.example = EXAMPLE
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 150)
        self.assertEqual(part1(self.input), None)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

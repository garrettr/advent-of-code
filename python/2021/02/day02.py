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
    horizontal_position = depth = aim = 0
    for line in input.strip().split("\n"):
        action, value = line.split()
        value = int(value)
        match action:
            case "down":
                aim += value
            case "up":
                aim -= value
            case "forward":
                horizontal_position += value
                depth += aim * value
    return horizontal_position * depth


class TestDay2(unittest.TestCase):
    def setUp(self):
        self.example = EXAMPLE
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 150)
        self.assertEqual(part1(self.input), 1727835)

    def test_part2(self):
        self.assertEqual(part2(self.example), 900)
        self.assertEqual(part2(self.input), 1544000595)


if __name__ == "__main__":
    unittest.main()

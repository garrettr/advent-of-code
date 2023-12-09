#!/usr/bin/env python3
from dataclasses import dataclass
from pprint import pprint
import itertools
import re
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 8


@dataclass
class Map:
    instructions: str
    nodes: dict[str, dict[str, str]]

    def navigate(self) -> int:
        current = "AAA"
        steps = 0
        for instruction in itertools.cycle(self.instructions):
            current = self.nodes[current][instruction]
            steps += 1
            if current == "ZZZ":
                return steps


def parse(input: str) -> Map:
    instructions, node_definitions = input.split("\n\n")
    node_re = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")
    nodes = {}
    for node_definition in node_definitions.splitlines():
        node, left, right = node_re.match(node_definition).groups()
        nodes[node] = {"L": left, "R": right}
    return Map(instructions, nodes)


def part1(input: str) -> int:
    map = parse(input)
    return map.navigate()


def part2(input: str):
    pass


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.example2 = get_puzzle_input(YEAR, DAY, "example2.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 2)
        self.assertEqual(part1(self.example2), 6)
        self.assertEqual(part1(self.input), 19667)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

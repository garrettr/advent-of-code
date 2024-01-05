#!/usr/bin/env python3
from dataclasses import dataclass
from pprint import pprint
import itertools
import math
import re
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 8


@dataclass
class Map:
    instructions: str
    nodes: dict[str, dict[str, str]]

    def navigate(self, start="AAA", end="ZZZ") -> int:
        current = start
        for step, instruction in enumerate(itertools.cycle(self.instructions)):
            current = self.nodes[current][instruction]
            if current.endswith(end):
                return step + 1

    def navigate2(self):
        start_nodes = (key for key in self.nodes.keys() if key.endswith("A"))
        path_lens = (self.navigate(start, "Z") for start in start_nodes)
        return math.lcm(*path_lens)


def parse(input: str) -> Map:
    instructions, node_definitions = input.split("\n\n")
    node_re = re.compile(r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)")
    nodes = {}
    for node_definition in node_definitions.splitlines():
        node, left, right = node_re.match(node_definition).groups()
        nodes[node] = {"L": left, "R": right}
    return Map(instructions, nodes)


def part1(input: str) -> int:
    map = parse(input)
    return map.navigate()


def part2(input: str):
    map = parse(input)
    return map.navigate2()


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.example2 = get_puzzle_input(YEAR, DAY, "example2.txt")
        self.example3 = get_puzzle_input(YEAR, DAY, "example3.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 2)
        self.assertEqual(part1(self.example2), 6)
        self.assertEqual(part1(self.input), 19667)

    def test_part2(self):
        self.assertEqual(part2(self.example3), 6)
        self.assertEqual(part2(self.input), 19185263738117)


if __name__ == "__main__":
    unittest.main()

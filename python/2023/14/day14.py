#!/usr/bin/env python3
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 14


def part1(input: str):
    rows = input.splitlines()
    cols = zip(*rows)

    # For each column, split into sections delimited by cube-shaped rocks (#) or the edges of the platform.
    # Keep track of the starting index of each section.
    # When the platform is tilted north, all rounded rocks (O) will fall to the beginning of their section.
    total_load = 0
    for col in cols:
        section_start = 0
        num_rounded_rocks = 0
        for i, c in enumerate(col):
            if c == "O":
                num_rounded_rocks += 1
            if c == "#" or i == len(col) - 1:
                total_load += sum(
                    range(
                        len(col) - section_start,
                        len(col) - section_start - num_rounded_rocks,
                        -1,
                    )
                )
                section_start = i + 1
                num_rounded_rocks = 0

    return total_load


def part2(input: str):
    pass


class TestDay14(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 136)
        self.assertEqual(part1(self.input), 105249)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

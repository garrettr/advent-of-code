#!/usr/bin/env python3
from itertools import pairwise
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 1
EXAMPLE = """199
200
208
210
200
207
240
269
260
263"""


def part1(input: str):
    "Count the number of times a depth measurement increases from the previous measurement."
    dms = [int(x) for x in input.splitlines()]
    return sum(x < y for (x, y) in pairwise(dms))


def part2(input: str):
    pass


class TestDay1(unittest.TestCase):
    def setUp(self):
        self.example = EXAMPLE
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 7)
        self.assertEqual(part1(self.input), None)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

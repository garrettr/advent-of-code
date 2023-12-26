#!/usr/bin/env python3
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 15
EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def hash(s: str) -> int:
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value = value % 256
    return value


def part1(input: str) -> int:
    return sum(hash(step) for step in input.replace("\n", "").split(","))


def part2(input: str):
    pass


class TestDay15(unittest.TestCase):
    def setUp(self):
        self.example = EXAMPLE
        self.input = get_puzzle_input(YEAR, DAY)

    def test_hash(self):
        self.assertEqual(hash("HASH"), 52)

    def test_part1(self):
        self.assertEqual(part1(self.example), 1320)
        self.assertEqual(part1(self.input), 511343)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

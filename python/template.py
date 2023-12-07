#!/usr/bin/env python3
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 1


def part1(input: str):
    pass


def part2(input: str):
    pass


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), "Fill me in!")
        # self.assertEqual(part1(self.input), None)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

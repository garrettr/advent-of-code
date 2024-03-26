#!/usr/bin/env python3
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 7


def part1(input: str):
    crabs = [int(x) for x in input.strip().split(",")]
    fuel_costs = [
        sum([abs(crab - position) for crab in crabs])
        for position in range(min(crabs), max(crabs))
    ]
    return min(fuel_costs)


def part2(input: str):
    pass


class TestDay7(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 37)
        self.assertEqual(part1(self.input), 341534)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

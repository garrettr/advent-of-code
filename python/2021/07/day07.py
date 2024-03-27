#!/usr/bin/env python3
from functools import cache
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


# Speed up part2 by:
# 1. Tracking the current min fuel cost instead of creating a list of all the
#    fuel costs and then finding the minimum of the list.
#    a) Result: 12.88s -> 12.86s! Not worth it!
# 2. Use closed form solution to compute sum of range.
#    a) Result: 12.88s -> 0.294s! Wow!!
# 3. Memoize computing the sum of a range.
#    a) Result: 0.294s -> 0.264s
@cache
def range_sum(n: int) -> int:
    return n * (n + 1) // 2


def part2(input: str):
    crabs = [int(x) for x in input.strip().split(",")]
    fuel_costs = [
        sum([range_sum(abs(crab - position)) for crab in crabs])
        for position in range(min(crabs), max(crabs))
    ]
    return min(fuel_costs)


class TestDay7(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 37)
        self.assertEqual(part1(self.input), 341534)

    def test_part2(self):
        self.assertEqual(part2(self.example), 168)
        self.assertEqual(part2(self.input), 93397632)


if __name__ == "__main__":
    unittest.main()

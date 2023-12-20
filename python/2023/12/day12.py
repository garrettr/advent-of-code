#!/usr/bin/env python3
from itertools import product
import re
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 12


def parse(input):
    return [
        (a, [int(n) for n in b.split(",")])
        for a, b in (line.split(" ") for line in input.splitlines())
    ]


def count_arrangements(row) -> int:
    springs, counts = row
    results = set()

    possibilities = []
    for spring in springs:
        if spring == "?":
            possibilities.append(["#", "."])
        else:
            possibilities.append([spring])

    for combo in product(*possibilities):
        candidate = "".join(combo)
        matches = re.findall(r"#+", candidate)
        match_lengths = [len(x) for x in matches]
        if match_lengths == counts:
            results.add(candidate)

    return len(results)


def part1(input: str):
    return sum(count_arrangements(row) for row in parse(input))


def part2(input: str):
    pass


class Test(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 21)
        self.assertEqual(part1(self.input), 7350)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

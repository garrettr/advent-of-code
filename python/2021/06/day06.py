#!/usr/bin/env python3
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 6


def parse(input: str) -> list[int]:
    return [int(x) for x in input.strip().split(",")]


def simulate(fishes: list[int], days: int):
    for day in range(days):
        new_fishes = []
        for i, fish in enumerate(fishes):
            if fish == 0:
                fishes[i] = 6
                new_fishes.append(8)
            else:
                fishes[i] = fish - 1
        fishes += new_fishes
    return fishes


def part1(input: str) -> int:
    fishes = parse(input)
    simulate(fishes, 80)
    return len(fishes)


def part2(input: str):
    pass


class TestDay6(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_simulate(self):
        self.assertEqual(len(simulate(parse(self.example), 18)), 26)

    def test_part1(self):
        self.assertEqual(part1(self.example), 5934)
        self.assertEqual(part1(self.input), 391671)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

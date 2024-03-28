#!/usr/bin/env python3
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 8


def parse(input: str):
    return [
        tuple(tuple(part.split(" ")) for part in line.split(" | "))
        for line in input.splitlines()
    ]


def part1(input: str):
    num_easy_digits = 0
    for _, output_value in parse(input):
        for digit in output_value:
            if len(digit) in (2, 3, 4, 7):
                num_easy_digits += 1
    return num_easy_digits


def part2(input: str):
    pass


class TestDay8(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 26)
        self.assertEqual(part1(self.input), 381)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

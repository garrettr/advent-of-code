#!/usr/bin/env python3
from collections import Counter
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 3


def parse(input: str) -> list[str]:
    return input.splitlines()


def part1(input: str):
    bits_by_position = zip(*parse(input))
    most_common_bits = [Counter(bits).most_common(1)[0][0] for bits in bits_by_position]
    least_common_bits = ["0" if bit == "1" else "1" for bit in most_common_bits]
    gamma_rate = int("".join(most_common_bits), 2)
    epsilon_rate = int("".join(least_common_bits), 2)
    return gamma_rate * epsilon_rate


def part2(input: str):
    pass


class TestDay3(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 198)
        self.assertEqual(part1(self.input), 2972336)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

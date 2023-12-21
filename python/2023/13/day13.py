#!/usr/bin/env python3
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 13


def reflection_row(block: list[str]) -> int:
    for idx in range(len(block)):
        if idx == 0:
            continue

        if all(l == r for l, r in zip(reversed(block[:idx]), block[idx:])):
            return idx

    return 0


def part1(input: str):
    vertical_reflections = horizontal_reflections = 0
    for pattern in (section.splitlines() for section in input.split("\n\n")):
        horizontal = reflection_row(pattern)
        vertical = reflection_row(list(zip(*pattern)))
        vertical_reflections += vertical if vertical else 0
        horizontal_reflections += 100 * horizontal if horizontal else 0
    return vertical_reflections + horizontal_reflections


def part2(input: str):
    pass


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 405)
        self.assertEqual(part1(self.input), 29213)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

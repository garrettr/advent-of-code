#!/usr/bin/env python3
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 13


def distance(l: str, r: str) -> int:
    return sum(a != b for a, b in zip(l, r))


def reflection_row(block: list[str], distance_to_match: int) -> int:
    for i in range(1, len(block)):
        if (
            sum(distance(l, r) for l, r in zip(reversed(block[:i]), block[i:]))
            == distance_to_match
        ):
            return i

    return 0


def score_block(block: str, distance_to_match: int) -> int:
    rows = block.splitlines()
    if row := reflection_row(rows, distance_to_match):
        return 100 * row

    if col := reflection_row(list(zip(*rows)), distance_to_match):
        return col

    raise ValueError("no reflection found!")


def part1(input: str):
    return sum(score_block(block, 0) for block in input.split("\n\n"))


def part2(input: str):
    return sum(score_block(block, 1) for block in input.split("\n\n"))


class TestDay13(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 405)
        self.assertEqual(part1(self.input), 29213)

    def test_part2(self):
        self.assertEqual(part2(self.example), 400)
        self.assertEqual(part2(self.input), 37453)


if __name__ == "__main__":
    unittest.main()

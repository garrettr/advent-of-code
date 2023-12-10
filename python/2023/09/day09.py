#!/usr/bin/env python3
from itertools import pairwise
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 9


def parse(input) -> list[list[int]]:
    return [[int(n) for n in line.split()] for line in input.splitlines()]


def next_in_seq(seq: list[int]):
    diff_seqs = [seq]
    while not all(n == 0 for n in diff_seqs[-1]):
        diff_seqs.append([y - x for x, y in pairwise(diff_seqs[-1])])

    diff_seqs[-1].append(0)
    for curr, prev in pairwise(reversed(diff_seqs)):
        prev.append(curr[-1] + prev[-1])

    return diff_seqs[0][-1]


def prev_in_seq(seq: list[int]):
    diff_seqs = [seq]
    while not all(n == 0 for n in diff_seqs[-1]):
        diff_seqs.append([y - x for x, y in pairwise(diff_seqs[-1])])

    diff_seqs[-1].insert(0, 0)
    for curr, prev in pairwise(reversed(diff_seqs)):
        prev.insert(0, prev[0] - curr[0])

    return diff_seqs[0][0]


def part1(input: str):
    return sum(next_in_seq(seq) for seq in parse(input))


def part2(input: str):
    return sum(prev_in_seq(seq) for seq in parse(input))


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 114)
        self.assertEqual(part1(self.input), 1789635132)

    def test_part2(self):
        self.assertEqual(part2(self.example), 2)
        self.assertEqual(part2(self.input), 913)


if __name__ == "__main__":
    unittest.main()

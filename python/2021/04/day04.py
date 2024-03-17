#!/usr/bin/env python3
from collections.abc import Iterable
from itertools import chain
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 4


def parse(input: str):
    parts = input.strip().split("\n\n")
    numbers = [int(x) for x in parts[0].split(",")]
    boards = [
        [[int(x) for x in line.split()] for line in part.split("\n")]
        for part in parts[1:]
    ]
    return numbers, boards


def won(board, numbers):
    assert len(numbers) >= 5
    numbers = set(numbers)
    for row in chain(board, zip(*board)):
        assert len(row) == 5
        if set(row) <= numbers:
            return True
    return False


def flatten(nested_list):
    for element in nested_list:
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            yield from flatten(element)
        else:
            yield element


def score(board, numbers):
    unmarked_numbers = set(flatten(board)) - set(numbers)
    return sum(unmarked_numbers) * numbers[-1]


def part1(input: str):
    numbers, boards = parse(input)
    for i in range(5, len(numbers)):
        drawn = numbers[:i]
        for board in boards:
            if won(board, drawn):
                return score(board, drawn)
    raise Exception("No solution found!")


def part2(input: str):
    numbers, boards = parse(input)
    for i in range(5, len(numbers)):
        drawn = numbers[:i]
        last_board = boards[-1]
        boards = [board for board in boards if not won(board, drawn)]
        if len(boards) == 0:
            return score(last_board, drawn)
    raise Exception("No solution found!")


class TestDay4(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 4512)
        self.assertEqual(part1(self.input), 58412)

    def test_part2(self):
        self.assertEqual(part2(self.example), 1924)
        self.assertEqual(part2(self.input), 10030)


if __name__ == "__main__":
    unittest.main()

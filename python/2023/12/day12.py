#!/usr/bin/env python3
from dataclasses import dataclass
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 12


@dataclass
class Row:
    condition_records: str
    damaged_groups: list[int]


def parse(input: str) -> list[Row]:
    return [
        Row(a, [int(n) for n in b.split(",")])
        for a, b in (line.split(" ") for line in input.splitlines())
    ]


def backtrack(a: list, k: int, input):
    print(a, k)
    if is_a_solution(a, k, input):
        process_solution(a, k, input)
    else:
        k += 1
        for candidate in construct_candidates(a, k, input):
            a[k] = candidate
            backtrack(a, k, input)


def get_damaged_groups(a: list[str]):
    return [len(s) for s in "".join(a).split(".") if s]


def valid_arrangement(a: list[str], damaged_groups: list[int]):
    return get_damaged_groups(a) == damaged_groups


def is_a_solution(a: list, k: int, input: Row):
    return k == len(input.condition_records) - 1


def construct_candidates(a: list, k: int, input: Row):
    if input.condition_records[k] == "?":
        return [".", "#"]
    return [input.condition_records[k]]


part1_num_solutions = 0


def process_solution(a: list, k: int, input: Row):
    if valid_arrangement(a, input.damaged_groups):
        global part1_num_solutions
        part1_num_solutions += 1


def part1(input: str):
    rows = parse(input)
    for i, row in enumerate(rows):
        print(i)
        a = list(row.condition_records)
        backtrack(a, -1, row)
    return part1_num_solutions


def part2(input: str):
    pass


class Test(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 21)
        # self.assertEqual(part1(self.input), None)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

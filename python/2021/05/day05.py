#!/usr/bin/env python3
from collections import Counter
from itertools import chain, repeat
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 5

GridPoint = tuple[int, int]
Line = tuple[GridPoint, GridPoint]


def parse(input: str) -> list[Line]:
    def parse_point(s: str) -> GridPoint:
        return GridPoint(int(x) for x in s.split(","))

    return [
        tuple(parse_point(p) for p in [s.strip() for s in line.split("->")])
        for line in input.splitlines()
    ]


def is_vertical_or_horizontal_line(line: Line) -> bool:
    return line[0][0] == line[1][0] or line[0][1] == line[1][1]


def points_on(line) -> list[GridPoint]:
    (x1, y1), (x2, y2) = line
    x_step = 1 if x1 < x2 else -1
    y_step = 1 if y1 < y2 else -1
    return [
        (x, y)
        for x, y in zip(
            range(x1, x2 + x_step, x_step) if x1 != x2 else repeat(x1),
            range(y1, y2 + y_step, y_step) if y1 != y2 else repeat(y2),
        )
    ]


def part1(input: str):
    lines = parse(input)
    lines = [line for line in lines if is_vertical_or_horizontal_line(line)]
    points = [points_on(line) for line in lines]
    counter = Counter(chain(*points))
    points_with_two_or_more_overlapping_lines = [
        point for (point, count) in counter.most_common() if count > 1
    ]
    return len(points_with_two_or_more_overlapping_lines)


def part2(input: str):
    lines = parse(input)
    points = [points_on(line) for line in lines]
    counter = Counter(chain(*points))
    points_with_two_or_more_overlapping_lines = [
        point for (point, count) in counter.most_common() if count > 1
    ]
    return len(points_with_two_or_more_overlapping_lines)


class TestDay5(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_parse(self):
        self.assertEqual(parse("0,9 -> 5,9"), [((0, 9), (5, 9))])
        self.assertEqual(
            parse("8,0 -> 0,8\n9,4 -> 3,4"), [((8, 0), (0, 8)), ((9, 4), (3, 4))]
        )

    def test_points_on(self):
        self.assertEqual(points_on(((0, 0), (0, 2))), [(0, 0), (0, 1), (0, 2)])
        self.assertEqual(points_on(((0, 0), (3, 0))), [(0, 0), (1, 0), (2, 0), (3, 0)])
        self.assertEqual(points_on(((1, 1), (3, 3))), [(1, 1), (2, 2), (3, 3)])
        self.assertEqual(points_on(((9, 7), (7, 9))), [(9, 7), (8, 8), (7, 9)])

    def test_part1(self):
        self.assertEqual(part1(self.example), 5)
        self.assertEqual(part1(self.input), 7414)

    def test_part2(self):
        self.assertEqual(part2(self.example), 12)
        self.assertEqual(part2(self.input), 19676)


if __name__ == "__main__":
    unittest.main()

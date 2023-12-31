#!/usr/bin/env python3
from dataclasses import dataclass
from itertools import pairwise
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 18

LatticePoint = tuple[int, int]
Direction = str

DIRECTION_OFFSETS: dict[Direction, LatticePoint] = {
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
}


def add_points(a: LatticePoint, b: LatticePoint) -> LatticePoint:
    return a[0] + b[0], a[1] + b[1]


def sub_points(a: LatticePoint, b: LatticePoint) -> LatticePoint:
    return a[0] - b[0], a[1] - b[1]


def multiply_point_by_scalar(point: LatticePoint, scalar: int) -> LatticePoint:
    return point[0] * scalar, point[1] * scalar


@dataclass
class Step:
    direction: Direction
    distance: int

    def starting_from(self, start: LatticePoint) -> LatticePoint:
        return add_points(
            start,
            multiply_point_by_scalar(DIRECTION_OFFSETS[self.direction], self.distance),
        )


Plan = list[Step]


def parse(input: str) -> Plan:
    return [
        Step(direction, int(distance))
        for direction, distance, _ in (line.split(" ") for line in input.splitlines())
    ]


def boundary_points(plan: Plan) -> list[LatticePoint]:
    points: list[LatticePoint] = [(0, 0)]
    for step in plan:
        points.append(step.starting_from(points[-1]))
    return points


def path_length(a: LatticePoint, b: LatticePoint) -> int:
    diff = sub_points(a, b)
    length = diff[0] if diff[0] != 0 else diff[1]
    return abs(length)


def area(outline: list[LatticePoint]) -> int:
    """
    Uses the shoelace formula to find the area of the outlined polygon.
    """
    assert len(outline) > 2 and outline[0] == outline[-1]
    return (
        abs(
            sum(
                (a[0] * b[1]) - (b[0] * a[1] + path_length(a, b))
                for a, b in pairwise(outline)
            )
            // 2
        )
        + 1
    )


def part1(input: str):
    dig_plan = parse(input)
    outline = boundary_points(dig_plan)
    return area(outline)


def parse2(input: str):
    def parse_line(line: str):
        hex_code = line.split(" ")[2].strip("()#")
        distance = int(hex_code[:5], 16)
        direction = "RDLU"[int(hex_code[5], 16)]
        return direction, distance

    return [Step(*parse_line(line)) for line in input.splitlines()]


def part2(input: str):
    return area(boundary_points(parse2(input)))


class TestDay18(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 62)
        self.assertEqual(part1(self.input), 48400)

    def test_part2(self):
        self.assertEqual(part2(self.example), 952408144115)
        self.assertEqual(part2(self.input), 72811019847283)


if __name__ == "__main__":
    unittest.main()

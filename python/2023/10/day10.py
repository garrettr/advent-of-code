#!/usr/bin/env python3
from enum import Enum
from itertools import pairwise
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 10

GridPoint = tuple[int, int]
Grid = dict[GridPoint, str]


def parse_grid(raw_grid: list[str]) -> Grid:
    """
    Returns 2-tuples of (row, col) with their value.

    (0, 0) ------> (0, 9)
      |              |
      |              |
      |              |
      |              |
      |              V
    (9, 0) ------> (9, 9)
    """
    result = {}

    for row, line in enumerate(raw_grid):
        for col, c in enumerate(line):
            result[row, col] = c

    return result


START = "S"


def find_start(grid: Grid) -> GridPoint:
    starts = [point for point, value in grid.items() if value == START]
    assert len(starts) == 1
    return starts[0]


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def opposite(self):
        return Direction((self.value + 2) % 4)


DIRECTION_OFFSETS: dict[Direction, GridPoint] = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
}


def add_points(a: GridPoint, b: GridPoint) -> GridPoint:
    return a[0] + b[0], a[1] + b[1]


PIPES: dict[str, tuple[Direction, Direction]] = {
    "|": (Direction.NORTH, Direction.SOUTH),
    "-": (Direction.EAST, Direction.WEST),
    "L": (Direction.NORTH, Direction.EAST),
    "J": (Direction.NORTH, Direction.WEST),
    "7": (Direction.SOUTH, Direction.WEST),
    "F": (Direction.SOUTH, Direction.EAST),
}

STRAIGHTS = ("|", "-")
BENDS = ("L", "J", "7", "F")


def find_loop(grid: Grid, start: GridPoint) -> list[GridPoint]:
    point = None
    heading = None

    # Find a valid pipe connected to the start.
    for direction in Direction:
        neighboring_point = add_points(start, DIRECTION_OFFSETS[direction])
        if neighboring_point not in grid:
            continue

        neighbor = grid[neighboring_point]
        if neighbor not in PIPES:
            continue

        if (neighbor in STRAIGHTS and direction in PIPES[neighbor]) or (
            neighbor in BENDS and direction.opposite in PIPES[neighbor]
        ):
            point = neighboring_point
            heading = direction
            break

    assert point is not None
    assert heading is not None

    loop: list[GridPoint] = [start]
    while point != start:
        loop.append(point)

        if grid[point] in BENDS:
            pipe = PIPES[grid[point]]
            heading = pipe[1] if heading.opposite == pipe[0] else pipe[0]

        point = add_points(point, DIRECTION_OFFSETS[heading])

    return loop


def part1(input: str):
    grid = parse_grid(input.splitlines())
    start = find_start(grid)
    return int(len(find_loop(grid, start)) / 2)


def enclosed_area(loop: list[GridPoint]) -> int:
    # Copy the loop and append the start point to the end for the shoelace formula.
    boundary = loop + [loop[0]]

    # Compute the area with the shoelace formula
    area = abs(sum((x1 * y2) - (x2 * y1) for (x1, y1), (x2, y2) in pairwise(boundary)) // 2)

    # Compute the number of interior points with Pick's theorem:
    # A = i + b / 2 - 1, where
    # A = area of polygon
    # i = number of interior points
    # b = number of boundary points
    return area - ((len(boundary) - 1) // 2) + 1


def part2(input: str):
    grid = parse_grid(input.splitlines())
    start = find_start(grid)
    loop = find_loop(grid, start)
    return enclosed_area(loop)


class TestDay10(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.example2 = get_puzzle_input(YEAR, DAY, "example2.txt")
        self.example3 = get_puzzle_input(YEAR, DAY, "example3.txt")
        self.example4 = get_puzzle_input(YEAR, DAY, "example4.txt")
        self.example5 = get_puzzle_input(YEAR, DAY, "example5.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 4)
        self.assertEqual(part1(self.example2), 8)
        self.assertEqual(part1(self.input), 6931)

    def test_part2(self):
        self.assertEqual(part2(self.example3), 4)
        self.assertEqual(part2(self.example4), 8)
        self.assertEqual(part2(self.example5), 10)
        self.assertEqual(part2(self.input), 357)


if __name__ == "__main__":
    unittest.main()

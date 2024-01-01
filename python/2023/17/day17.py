#!/usr/bin/env python3
from dataclasses import dataclass
from enum import IntEnum
from heapq import heappop, heappush
from typing import Literal
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 17

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


Rotation = Literal["CCW", "CW"]


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def rotate(facing: "Direction", towards: Rotation) -> "Direction":
        offset = 1 if towards == "CW" else -1
        return Direction((facing.value + offset) % 4)

    @staticmethod
    def offset(facing: "Direction") -> GridPoint:
        return _ROW_COL_OFFSETS[facing]


_ROW_COL_OFFSETS: dict[Direction, GridPoint] = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}


def add_points(a: GridPoint, b: GridPoint) -> GridPoint:
    return a[0] + b[0], a[1] + b[1]


# Position needs to be comparable to be used with heapq.
# There are two easy ways to achieve this:
# 1. Add `order=True` to the dataclass decorator, as shown below.
# 2. Switch from dataclasses to NamedTuple (from typing).
@dataclass(frozen=True, order=True)
class Position:
    loc: GridPoint
    facing: Direction

    @property
    def next_loc(self) -> GridPoint:
        return add_points(self.loc, Direction.offset(self.facing))

    def step(self) -> "Position":
        return Position(self.next_loc, self.facing)

    def rotate_and_step(self, towards: Rotation) -> "Position":
        return Position(self.loc, Direction.rotate(self.facing, towards)).step()


State = tuple[int, Position, int]


def _solve(input: str, min_steps: int, max_steps: int) -> int:
    raw_grid = input.splitlines()

    # Bottom-right corner of the grid.
    target = len(raw_grid) - 1, len(raw_grid[0]) - 1
    grid = {k: int(v) for k, v in parse_grid(raw_grid).items()}

    # Start walking in both directions.
    queue: list[State] = [
        (0, Position((0, 0), Direction.DOWN), 0),
        (0, Position((0, 0), Direction.RIGHT), 0),
    ]
    seen: set[tuple[Position, int]] = set()

    while queue:
        cost, pos, num_steps = heappop(queue)

        if pos.loc == target and num_steps >= min_steps:
            return cost

        if (pos, num_steps) in seen:
            continue
        seen.add((pos, num_steps))

        if (
            num_steps >= min_steps
            and (left := pos.rotate_and_step("CCW")).loc in grid
        ):
            heappush(queue, (cost + grid[left.loc], left, 1))

        if (
            num_steps >= min_steps
            and (right := pos.rotate_and_step("CW")).loc in grid
        ):
            heappush(queue, (cost + grid[right.loc], right, 1))

        if num_steps < max_steps and (forward := pos.step()).loc in grid:
            heappush(queue, (cost + grid[forward.loc], forward, num_steps + 1))

    return -1


def part1(input: str) -> int:
    return _solve(input, 0, 3)


def part2(input: str):
    return _solve(input, 4, 10)


class TestDay17(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.example2 = get_puzzle_input(YEAR, DAY, "example2.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 102)
        self.assertEqual(part1(self.input), 1263)

    def test_part2(self):
        self.assertEqual(part2(self.example), 94)
        self.assertEqual(part2(self.example2), 71)
        self.assertEqual(part2(self.input), 1411)


if __name__ == "__main__":
    unittest.main()

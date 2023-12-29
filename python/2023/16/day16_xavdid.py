#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum
from typing import Literal
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 16

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


def add_points(a: GridPoint, b: GridPoint) -> GridPoint:
    """
    Add a pair of 2-tuples together.
    Useful for calculating a new position from a location and an offset.
    """
    return a[0] + b[0], a[1] + b[1]


Rotation = Literal["CCW", "CW"]


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def rotate(facing: "Direction", towards: Rotation) -> "Direction":
        offset = 1 if towards == "CW" else -1
        return Direction((facing.value + offset) % 4)

    
ROW_COLL_OFFSETS: dict[Direction, GridPoint] = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}


@dataclass(frozen=True)
class State:
    loc: GridPoint
    facing: Direction

    @property
    def next_loc(self) -> GridPoint:
        return add_points(self.loc, ROW_COLL_OFFSETS[self.facing])

    def step(self) -> "State":
        return State(self.next_loc, self.facing)

    def rotate_and_step(self, towards: Rotation) -> "State":
        return State(self.loc, Direction.rotate(self.facing, towards)).step()

    def next_states(self, char: str) -> list["State"]:
        match char:
            case ".":
                return [self.step()]
            # Ignore the pointy end of a splitter.
            case "-" if self.facing in (Direction.LEFT, Direction.RIGHT):
                return [self.step()]
            case "|" if self.facing in (Direction.UP, Direction.DOWN):
                return [self.step()]
            # Split on splitters we didn't pass over.
            case "-" | "|":
                return [
                    self.rotate_and_step("CCW"),
                    self.rotate_and_step("CW"),
                ]
            # Bounce off mirrors.
            case "/" if self.facing in (Direction.LEFT, Direction.RIGHT):
                return [self.rotate_and_step("CCW")]
            case "\\" if self.facing in (Direction.LEFT, Direction.RIGHT):
                return [self.rotate_and_step("CW")]
            case "/" if self.facing in (Direction.UP, Direction.DOWN):
                return [self.rotate_and_step("CW")]
            case "\\" if self.facing in (Direction.UP, Direction.DOWN):
                return [self.rotate_and_step("CCW")]
            case _:
                raise ValueError(
                    f"Unable to calculate next step from {self} and {char=}"
                )

    
def part1(input: str) -> int:
    grid = parse_grid(input.splitlines())

    seen: set[State] = set()
    queue: list[State] = [State((0, 0), Direction.RIGHT)]

    while queue:
        current = queue.pop()
        if current in seen:
            continue
        seen.add(current)

        for next_state in current.next_states(grid[current.loc]):
            if next_state.loc in grid:
                queue.append(next_state)

    return len({state.loc for state in seen})


class TestDay16(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 46)
        self.assertEqual(part1(self.input), 7242)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

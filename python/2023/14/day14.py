#!/usr/bin/env python3
from enum import Enum
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 14


def total_load_on_north_support_beams(platform: list[str]):
    cols = zip(*platform)

    # For each column, split into sections delimited by cube-shaped rocks (#) or the edges of the platform.
    # Keep track of the starting index of each section.
    # When the platform is tilted north, all rounded rocks (O) will fall to the beginning of their section.
    total_load = 0
    for col in cols:
        section_start = 0
        num_rounded_rocks = 0
        for i, c in enumerate(col):
            if c == "O":
                num_rounded_rocks += 1
            if c == "#" or i == len(col) - 1:
                total_load += sum(
                    range(
                        len(col) - section_start,
                        len(col) - section_start - num_rounded_rocks,
                        -1,
                    )
                )
                section_start = i + 1
                num_rounded_rocks = 0

    return total_load


def part1(input: str):
    return total_load_on_north_support_beams(input.splitlines())


class GridItem(Enum):
    EMPTY_SPACE = 0
    ROUNDED_ROCK = 1
    CUBE_SHAPED_ROCK = 2

    @classmethod
    def from_str(cls, s: str):
        return cls(".O#".index(s))


Row = tuple[GridItem, ...]
Grid = list[Row]


def parse_grid(raw_grid: list[str]) -> Grid:
    return [Row([GridItem.from_str(c) for c in line]) for line in raw_grid]


def tilt(row: Row) -> Row:
    "Tilt row to the left"
    tilted = []
    num_rounded_rocks = num_empty_spaces = 0

    for item in row:
        match item:
            case GridItem.EMPTY_SPACE:
                num_empty_spaces += 1
            case GridItem.ROUNDED_ROCK:
                num_rounded_rocks += 1
            case GridItem.CUBE_SHAPED_ROCK:
                tilted.extend([GridItem.ROUNDED_ROCK for _ in range(num_rounded_rocks)])
                tilted.extend([GridItem.EMPTY_SPACE for _ in range(num_empty_spaces)])
                num_rounded_rocks = num_empty_spaces = 0
                tilted.append(GridItem.CUBE_SHAPED_ROCK)

    if num_empty_spaces or num_rounded_rocks:
        tilted.extend([GridItem.ROUNDED_ROCK for _ in range(num_rounded_rocks)])
        tilted.extend([GridItem.EMPTY_SPACE for _ in range(num_empty_spaces)])

    return Row(tilted)


def cycle(platform: Grid) -> Grid:
    "Return the result of tilting the platform North, then West, then South, then East."
    # North
    transpose = zip(*platform)
    platform = [tilt(row) for row in transpose]
    # West
    transpose = zip(*platform)
    platform = [tilt(row) for row in transpose]
    # South
    transpose = [tuple(reversed(row)) for row in zip(*platform)]
    platform = [tilt(row) for row in transpose]
    # East
    platform = [tuple(reversed(row)) for row in platform]
    transpose = [tuple(reversed(row)) for row in zip(*platform)]
    platform = [tilt(row) for row in transpose]
    # Return to original orientation
    return [tuple(reversed(row)) for row in platform]


def print_grid(grid: Grid) -> None:
    for line in grid:
        print("".join(".O#"[item.value] for item in line))


def part2(input: str):
    grid = parse_grid(input.splitlines())
    states = {}
    state_cycle_start = state_cycle_end = None
    cycles = 1_000_000_000
    for i in range(cycles):
        if i % 1000 == 0:
            print(f"{i}/{cycles}")

        tuple_grid = tuple(grid)
        if tuple_grid in states:
            state_cycle_start = states[tuple_grid]
            state_cycle_end = i
            states[tuple_grid] = i
            break

        states[tuple_grid] = i
        grid = cycle(grid)

    state_cycle_step_after_cycles = cycles % (state_cycle_end - state_cycle_start)
    states_by_step = {step: state for state, step in states.items()}
    grid = states_by_step[state_cycle_step_after_cycles]
    for step, state in states_by_step.items():
        print(
            step,
            total_load_on_north_support_beams(
                ["".join([".O#"[item.value] for item in line]) for line in state]
            ),
        )
    return total_load_on_north_support_beams(
        ["".join([".O#"[item.value] for item in line]) for line in grid]
    )


class TestDay14(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 136)
        self.assertEqual(part1(self.input), 105249)

    def test_part2(self):
        self.assertEqual(part2(self.example), 64)
        # self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

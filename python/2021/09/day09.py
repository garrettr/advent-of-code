#!/usr/bin/env python3
from functools import reduce
from operator import mul
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 9

GridPoint = tuple[int, int]
Grid = dict[GridPoint, int]


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
    return {
        (row, col): int(c)
        for row, line in enumerate(raw_grid)
        for col, c in enumerate(line)
    }


def find_adjacent_points(grid: Grid, point: GridPoint) -> list[GridPoint]:
    def find_candidates(point):
        return [
            (point[0] + x, point[1] + y) for (x, y) in zip((-1, 1, 0, 0), (0, 0, -1, 1))
        ]

    return [candidate for candidate in find_candidates(point) if candidate in grid]


def find_low_points(grid: Grid) -> list[GridPoint]:
    low_points = []
    for point, height in grid.items():
        adjacent_points = find_adjacent_points(grid, point)
        heights = [grid[point] for point in adjacent_points]
        if height < min(heights):
            low_points.append(point)
    return low_points


def part1(input: str):
    grid = parse_grid(input.splitlines())
    low_points = find_low_points(grid)
    return sum(grid[point] + 1 for point in low_points)


def find_basins(grid: Grid) -> list[set[GridPoint]]:
    basins = []
    for low_point in find_low_points(grid):
        basin = set()
        candidates = set([low_point])
        while candidates:
            point = candidates.pop()
            if grid[point] < 9:
                basin.add(point)
                candidates.update(set(find_adjacent_points(grid, point)) - basin)
        basins.append(basin)
    return basins


def part2(input: str):
    grid = parse_grid(input.splitlines())
    basins = find_basins(grid)
    basins.sort(key=len, reverse=True)
    return reduce(mul, (len(basin) for basin in basins[:3]))


class TestDay9(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 15)
        self.assertEqual(part1(self.input), 458)

    def test_part2(self):
        self.assertEqual(part2(self.example), 1134)
        self.assertEqual(part2(self.input), 1391940)


if __name__ == "__main__":
    unittest.main()

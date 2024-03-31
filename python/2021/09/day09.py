#!/usr/bin/env python3
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


def part1(input: str):
    grid = parse_grid(input.splitlines())
    low_points_heights = []
    for point, height in grid.items():
        adjacent_points = find_adjacent_points(grid, point)
        heights = [grid[point] for point in adjacent_points]
        if height < min(heights):
            low_points_heights.append(height)
    return sum(height + 1 for height in low_points_heights)


def part2(input: str):
    pass


class TestDay9(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 15)
        self.assertEqual(part1(self.input), 458)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
from collections import defaultdict
from copy import copy
from operator import itemgetter
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 16


def valid_beam(grid, beam):
    return (
        beam[0] >= 0 and beam[1] >= 0 and beam[0] < len(grid) and beam[1] < len(grid[0])
    )


def part1(input: str):
    grid = input.splitlines()
    energized_tiles = defaultdict(int)
    beams = [[0, 0, "R", 0]]
    unique_beams = set()
    unique_beams.add(tuple(beams[0][:3]))

    steps = 0
    while beams:
        steps += 1
        if steps % 100 == 0:
            sorted_beams = sorted(beams, key=itemgetter(3), reverse=True)
            print(
                f"len(beams) = {len(beams)}, longest beam = {sorted_beams[0][3]}/{len(grid) * len(grid[0])}"
            )

        splits = []
        for bi, beam in enumerate(beams):
            row, col, heading, tiles_visited = beam
            energized_tiles[(row, col)] += 1
            split = None

            match grid[row][col]:
                case ".":
                    match heading:
                        case "L":
                            beam[1] -= 1
                        case "R":
                            beam[1] += 1
                        case "U":
                            beam[0] -= 1
                        case "D":
                            beam[0] += 1
                case "/":
                    match heading:
                        case "L":
                            beam[0] += 1
                            beam[2] = "D"
                        case "R":
                            beam[0] -= 1
                            beam[2] = "U"
                        case "U":
                            beam[1] += 1
                            beam[2] = "R"
                        case "D":
                            beam[1] -= 1
                            beam[2] = "L"
                case "\\":
                    match heading:
                        case "L":
                            beam[0] -= 1
                            beam[2] = "U"
                        case "R":
                            beam[0] += 1
                            beam[2] = "D"
                        case "U":
                            beam[1] -= 1
                            beam[2] = "L"
                        case "D":
                            beam[1] += 1
                            beam[2] = "R"
                case "|":
                    match heading:
                        case "L" | "R":
                            split = copy(beam)
                            beam[0] -= 1
                            beam[2] = "U"
                            split[0] += 1
                            split[2] = "D"
                        case "U":
                            beam[0] -= 1
                        case "D":
                            beam[0] += 1
                case "-":
                    match heading:
                        case "L":
                            beam[1] -= 1
                        case "R":
                            beam[1] += 1
                        case "U" | "D":
                            split = copy(beam)
                            beam[1] -= 1
                            beam[2] = "L"
                            split[1] += 1
                            split[2] = "R"

            if valid_beam(grid, beam) and tiles_visited < len(grid) * len(grid[0]):
                beam[3] += 1
            else:
                del beams[bi]

            if (
                split
                and valid_beam(grid, split)
                and tuple(split[:3]) not in unique_beams
            ):
                splits.append(split)
                unique_beams.add(tuple(split[:3]))

        beams.extend(splits)

    # print(energized_tiles)
    return len(energized_tiles)


def part2(input: str):
    pass


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

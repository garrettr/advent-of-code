#!/usr/bin/env python3
import itertools
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 11


def part1(input: str):
    def find_empty_space(lines) -> set[int]:
        return {i for i, line in enumerate(lines) if all(c == "." for c in line)}

    rows = input.splitlines()
    rows_to_expand = find_empty_space(rows)
    cols_to_expand = find_empty_space(zip(*rows))

    galaxies = [
        (ri, ci)
        for ri, row in enumerate(rows)
        for ci, col in enumerate(row)
        if col == "#"
    ]

    shortest_path_lens = []
    for g1, g2 in itertools.combinations(galaxies, 2):
        shortest_path_len = 0
        for r in range(*sorted((g1[0], g2[0]))):
            if r in rows_to_expand:
                shortest_path_len += 2
            else:
                shortest_path_len += 1
        for c in range(*sorted((g1[1], g2[1]))):
            if c in cols_to_expand:
                shortest_path_len += 2
            else:
                shortest_path_len += 1
        # print(f"{g1} -> {g2}: {shortest_path_len}")
        shortest_path_lens.append(shortest_path_len)

    return sum(shortest_path_lens)

    # The following functional-style code is correct on the example input,
    # but much slower on `input.txt` than the above imperative-style code.
    # TODO: why?
    # def shortest_path(g1, g2):
    #     return sum(
    #         2 if i in indices_to_expand else 1
    #         for indices_to_expand, dimension in zip(
    #             (rows_to_expand, cols_to_expand),
    #             zip(g1, g2),
    #         )
    #         for i in range(*sorted(dimension))
    #     )

    # return sum(shortest_path(g1, g2) for g1, g2 in itertools.combinations(galaxies, 2))


def part2(input: str):
    pass


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 374)
        self.assertEqual(part1(self.input), 10313550)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

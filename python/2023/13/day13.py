#!/usr/bin/env python3
from itertools import pairwise
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 13


def find_potential_reflections(pattern):
    return [i for i, pair in enumerate(pairwise(pattern)) if pair[0] == pair[1]]


def valid_reflection(pattern, reflection):
    steps = 1
    for i in range(reflection):
        lo = reflection - i - 1
        hi = reflection + i + 2
        try:
            if pattern[lo] != pattern[hi]:
                return False
        except IndexError:
            break
        steps += 1
    return steps


def find_reflection(pattern):
    candidate = None
    for reflection in find_potential_reflections(pattern):
        if width := valid_reflection(pattern, reflection):
            if not candidate or candidate[1] < width:
                candidate = (reflection, width)
    return candidate


def part1(input: str):
    patterns = [section.splitlines() for section in input.split("\n\n")]
    reflections = []
    for i, pattern in enumerate(patterns):
        vref = find_reflection(list(zip(*pattern)))
        href = find_reflection(pattern)

        if vref and href:
            if vref[1] > href[1]:
                reflections.append(("v", vref[0]))
            else:
                reflections.append(("h", href[0]))
        elif vref:
            reflections.append(("v", vref[0]))
        elif href:
            reflections.append(("h", href[0]))
        else:
            # raise ValueError(f"No reflection found for pattern: \n{'\n'.join(pattern)}")
            print(f"No reflection found for {i}: \n{'\n'.join(pattern)}\n")

    # pprint(reflections)
    return sum(i + 1 if type == "v" else (i + 1) * 100 for type, i in reflections)


def part2(input: str):
    pass


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 405)
        self.assertEqual(part1(self.input), 29213)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
from collections import defaultdict
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 8


def parse(input: str):
    return [
        tuple(tuple(part.split(" ")) for part in line.split(" | "))
        for line in input.splitlines()
    ]


def part1(input: str):
    return sum(
        [
            1 if len(digit) in (2, 3, 4, 7) else 0
            for _, output_value in parse(input)
            for digit in output_value
        ]
    )


DIGITS = {
    frozenset("abcefg"): 0,
    frozenset("cf"): 1,
    frozenset("acdeg"): 2,
    frozenset("acdfg"): 3,
    frozenset("bcdf"): 4,
    frozenset("abdfg"): 5,
    frozenset("abdefg"): 6,
    frozenset("acf"): 7,
    frozenset("abcdefg"): 8,
    frozenset("abcdfg"): 9,
}


def analyze(note):
    patterns, _ = note
    mapping = {}

    patterns_by_len = defaultdict(list)
    for pattern in patterns:
        patterns_by_len[len(pattern)].append(set(pattern))

    # Extract known digits with unique lengths.
    digit1 = patterns_by_len[2][0]
    digit4 = patterns_by_len[4][0]
    digit7 = patterns_by_len[3][0]
    digit8 = patterns_by_len[7][0]

    # Find 'a'
    # Digit 1 (len 2) uses segments c, f
    # Digit 7 (len 3) uses segments a, c, f
    mapping["a"] = (digit7 - digit1).pop()

    # Find 'c'
    # Digit 6 (len 6) uses segments a, b, d, e, f, g
    # Digit 1 (len 2) uses segments c, f
    for digit in patterns_by_len[6]:
        diff = digit1 - digit
        if len(diff):
            mapping["c"] = diff.pop()
            break

    # Find 'f'
    mapping["f"] = (digit1 - set(mapping["c"])).pop()

    # Find 'g'
    # Digit 9 (len 6) uses segments a, b, c, d, f, g
    # Digit 4 (len 4) uses segments b, c, d, f
    for digit in patterns_by_len[6]:
        diff = digit - digit4 - set(mapping["a"])
        if len(diff) == 1:
            mapping["g"] = diff.pop()
            break

    # Find 'e'
    # Digit 8 (len 7) uses segments a, b, c, d, e, f, g
    # Digit 9 (len 6) uses segments a, b, c, d, f, g
    # Digit 6 (len 6) uses segments a, b, d, e, f, g
    # Digit 0 (len 6) uses segments a, b, c, e, f, g
    for digit in patterns_by_len[6]:
        diff = digit8 - digit - digit4
        if len(diff):
            mapping["e"] = diff.pop()
            break

    # Find 'b'
    # Digit 0 (len 6) uses segments a, b, c, e, f, g
    # We now know acefg, so 0 - acefg = b.
    # Digit 6 - acefg = bd
    # Digit 9 - acefg = bd
    for digit in patterns_by_len[6]:
        diff = digit - set(mapping.values())
        if len(diff) == 1:
            mapping["b"] = diff.pop()
            # Must break after updating mapping!
            break

    # Finally, find 'd'.
    mapping["d"] = (digit8 - set(mapping.values())).pop()

    # Sanity check: each mapping value should be unique.
    assert len(mapping.values()) == len(set(mapping.values()))

    # Flip the dictionary so we can look up the true segments from the scrambled
    # segments.
    return {v: k for k, v in mapping.items()}


def decode(output_value, mapping):
    digits = []
    for digit in output_value:
        segments = frozenset(mapping[segment] for segment in digit)
        digits.append(DIGITS[segments])
    return int("".join(map(str, digits)))


def part2(input: str):
    notes = parse(input)
    mappings = [analyze(note) for note in notes]
    return sum(
        [
            decode(output_value, mapping)
            for ((_, output_value), mapping) in zip(notes, mappings)
        ]
    )


class TestDay8(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 26)
        self.assertEqual(part1(self.input), 381)

    def test_part2(self):
        self.assertEqual(part2(self.example), 61229)
        self.assertEqual(part2(self.input), 1023686)


if __name__ == "__main__":
    unittest.main()

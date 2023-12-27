#!/usr/bin/env python3
from collections import defaultdict
import re
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 15
EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def hash(s: str) -> int:
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value = value % 256
    return value


def part1(input: str) -> int:
    return sum(hash(step) for step in input.replace("\n", "").split(","))


STEP_RE = r"(?P<label>[a-z]+)(?P<operation>=|-)(?P<focal_length>[1-9])?"


def print_boxes(boxes):
    for box, lenses in boxes.items():
        print(
            f"Box {box}:",
            *[f"[{label} {focal_length}]" for label, focal_length in lenses.items()],
        )


def initialization_sequence(input: str, verbose=False):
    steps = input.replace("\n", "").split(",")
    boxes = defaultdict(dict)

    for step in steps:
        label, operation, focal_length = re.match(STEP_RE, step).groups()
        box = hash(label)
        match operation:
            case "-":
                if label in boxes[box]:
                    del boxes[box][label]
            case "=":
                boxes[box][label] = int(focal_length)

        if verbose:
            print(f'After "{step}":')
            print_boxes(boxes)
            print()

    return boxes


def focusing_power(boxes):
    return sum(
        (box + 1) * (lens + 1) * focal_length
        for box, lenses in boxes.items()
        for lens, (_, focal_length) in enumerate(lenses.items())
    )


def part2(input: str):
    boxes = initialization_sequence(input)
    return focusing_power(boxes)


class TestDay15(unittest.TestCase):
    def setUp(self):
        self.example = EXAMPLE
        self.input = get_puzzle_input(YEAR, DAY)

    def test_hash(self):
        self.assertEqual(hash("HASH"), 52)

    def test_part1(self):
        self.assertEqual(part1(self.example), 1320)
        self.assertEqual(part1(self.input), 511343)

    def test_part2(self):
        self.assertEqual(part2(self.example), 145)
        self.assertEqual(part2(self.input), 294474)


if __name__ == "__main__":
    unittest.main()

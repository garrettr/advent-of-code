#!/usr/bin/env python3
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 6


@dataclass
class Race:
    duration: int
    record_distance: int


def parse(input: str) -> list[Race]:
    times, distances = [
        [int(n) for n in line.split(":")[1].strip().split()]
        for line in input.strip().splitlines()
    ]
    return [Race(time, distance) for time, distance in zip(times, distances)]


def number_of_ways_to_beat(race: Race) -> int:
    return sum(
        (
            (t * (race.duration - t)) > race.record_distance
            for t in range(1, race.duration)
        )
    )


def part1(input: str) -> int:
    races = parse(input)
    return reduce(mul, (number_of_ways_to_beat(race) for race in races))


def parse2(input: str) -> Race:
    time, distance = [
        int("".join(line.split(":")[1].strip().split()))
        for line in input.strip().splitlines()
    ]
    return Race(time, distance)


def part2(input: str):
    race = parse2(input)
    return number_of_ways_to_beat(race)


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 288)
        self.assertEqual(part1(self.input), 781200)

    def test_part2(self):
        self.assertEqual(part2(self.example), 71503)
        self.assertEqual(part2(self.input), 49240091)


if __name__ == "__main__":
    unittest.main()

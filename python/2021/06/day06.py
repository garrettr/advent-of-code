#!/usr/bin/env python3
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 6


def parse(input: str) -> list[int]:
    return [int(x) for x in input.strip().split(",")]


def parse2(input: str) -> list[int]:
    # Instead of tracking each individual fish, just keep track of the sum of
    # fish per day in the 7 day cycle. Add 2 days to the cycle for new fish,
    # which spawn with their internal timer set to 8 days.
    cycle = [0] * 9
    for fish in input.strip().split(","):
        cycle[int(fish)] += 1
    return cycle


def simulate(fishes: list[int], days: int):
    for day in range(days):
        new_fishes = []
        for i, fish in enumerate(fishes):
            if fish == 0:
                fishes[i] = 6
                new_fishes.append(8)
            else:
                fishes[i] = fish - 1
        fishes += new_fishes
    return fishes


def simulate2(cycle: list[int], days: int):
    for _ in range(days):
        # Aging
        prev_day_count = cycle[-1]
        for day in reversed(range(1, len(cycle))):
            curr_day_count = prev_day_count
            prev_day_count = cycle[day - 1]
            cycle[day] -= curr_day_count
            cycle[day - 1] += curr_day_count
        # Spawning
        cycle[0] -= prev_day_count
        cycle[6] += prev_day_count
        cycle[8] += prev_day_count
    return cycle


def part1(input: str) -> int:
    fishes = parse(input)
    simulate(fishes, 80)
    return len(fishes)


def part2(input: str):
    cycle = parse2(input)
    simulate2(cycle, 256)
    return sum(cycle)


class TestDay6(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_simulate(self):
        self.assertEqual(len(simulate(parse(self.example), 18)), 26)

    def test_parse2(self):
        self.assertEqual(parse2(self.example), [0, 1, 1, 2, 1, 0, 0, 0, 0])

    def test_part1(self):
        self.assertEqual(part1(self.example), 5934)
        self.assertEqual(part1(self.input), 391671)

    def test_simulate2(self):
        self.assertEqual(sum(simulate2(parse2(self.example), 80)), 5934)
        self.assertEqual(sum(simulate2(parse2(self.input), 80)), 391671)

    def test_part2(self):
        self.assertEqual(part2(self.example), 26984457539)
        self.assertEqual(part2(self.input), 1754000560399)


if __name__ == "__main__":
    unittest.main()

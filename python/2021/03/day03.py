#!/usr/bin/env python3
from collections import Counter
import unittest

from advent import get_puzzle_input

YEAR = 2021
DAY = 3


def parse(input: str) -> list[str]:
    return input.splitlines()


def part1(input: str):
    bits_by_position = zip(*parse(input))
    most_common_bits = [Counter(bits).most_common(1)[0][0] for bits in bits_by_position]
    least_common_bits = ["0" if bit == "1" else "1" for bit in most_common_bits]
    gamma_rate = int("".join(most_common_bits), 2)
    epsilon_rate = int("".join(least_common_bits), 2)
    return gamma_rate * epsilon_rate


def most_common_value(values):
    values_sorted_by_count = Counter(values).most_common()
    if values_sorted_by_count[0][1] == values_sorted_by_count[1][1]:
        return "1"
    return values_sorted_by_count[0][0]


def least_common_value(values):
    values_sorted_by_count = Counter(values).most_common()
    if values_sorted_by_count[0][1] == values_sorted_by_count[1][1]:
        return "0"
    return values_sorted_by_count[1][0]


def part2(input: str):
    def filter_values(values: list[int], position: int, criterion):
        if len(values) == 1:
            return values[0]
        values_by_position = list(zip(*values))
        required_value = criterion(values_by_position[position])
        filtered_values = [
            value for value in values if value[position] == required_value
        ]
        # print(filtered_values)
        return filter_values(filtered_values, position + 1, criterion)

    values = parse(input)
    o2_generator_rating = filter_values(values, 0, most_common_value)
    co2_scrubber_rating = filter_values(values, 0, least_common_value)
    o2_generator_rating = int("".join(o2_generator_rating), 2)
    co2_scrubber_rating = int("".join(co2_scrubber_rating), 2)
    return o2_generator_rating * co2_scrubber_rating


class TestDay3(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 198)
        self.assertEqual(part1(self.input), 2972336)

    def test_part2(self):
        self.assertEqual(part2(self.example), 230)
        self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

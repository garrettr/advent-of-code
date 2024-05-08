#!/usr/bin/env python3
from dataclasses import dataclass
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 4


@dataclass
class ScratchCard:
    id: int
    winning_numbers: set[int]
    numbers_you_have: set[int]

    @classmethod
    def from_str(cls, s: str):
        id = int(s.split(":")[0].split()[1])
        number_lists = s.split(":")[1].strip().split("|")
        numbers = [
            {int(n) for n in number_list.split()} for number_list in number_lists
        ]
        return cls(id, *numbers)

    @property
    def matches(self) -> int:
        return len(self.winning_numbers & self.numbers_you_have)

    @property
    def score(self) -> int:
        return 2 ** (self.matches - 1) if self.matches else 0


def parse_cards(input: str) -> list[ScratchCard]:
    return [ScratchCard.from_str(line) for line in input.splitlines()]


def part1(input: str):
    return sum(card.score for card in parse_cards(input))


def part2(input: str):
    cards = parse_cards(input)
    card_counts = [1] * len(cards)
    for i, card in enumerate(cards):
        for j in range(0, card.matches):
            card_counts[i + j + 1] += card_counts[i]
    return sum(card_counts)


class TestDay04(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 13)
        self.assertEqual(part1(self.input), 21919)

    def test_part2(self):
        self.assertEqual(part2(self.example), 30)
        self.assertEqual(part2(self.input), 9881048)


if __name__ == "__main__":
    unittest.main()

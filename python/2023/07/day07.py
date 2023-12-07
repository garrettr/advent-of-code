#!/usr/bin/env python3
from collections import Counter
from dataclasses import dataclass
import enum
import functools
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 7


@functools.total_ordering
class Type(enum.Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


@dataclass
class Hand:
    hand: str
    bid: int

    CARD_LABELS = "23456789TJQKA"

    @property
    def type(self) -> Type:
        assert len(self.hand) == 5
        counter = Counter(self.hand)
        counts = set(counter.values())
        match len(counter):
            case 1:
                return Type.FIVE_OF_A_KIND
            case 2:
                if counts == {4, 1}:
                    return Type.FOUR_OF_A_KIND
                elif counts == {3, 2}:
                    return Type.FULL_HOUSE
                else:
                    raise ValueError(f"Failed to determine type of hand: {self.hand}")
            case 3:
                if counts == {3, 1, 1}:
                    return Type.THREE_OF_A_KIND
                if counts == {2, 2, 1}:
                    return Type.TWO_PAIR
                else:
                    raise ValueError(f"Failed to determine type of hand: {self.hand}")
            case 4:
                return Type.ONE_PAIR
            case 5:
                return Type.HIGH_CARD
            case _:
                raise ValueError(f"Failed to determine type of hand: {self.hand}")

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if self.type != other.type:
                return self.type < other.type
            else:
                for self_card, other_card in zip(self.hand, other.hand):
                    if self_card != other_card:
                        return self.CARD_LABELS.index(
                            self_card
                        ) < self.CARD_LABELS.index(other_card)

        return NotImplemented


@dataclass
class Game:
    hands: list[Hand]

    @classmethod
    def from_str(cls, s: str):
        return cls(
            [
                Hand(hand, int(bid))
                for hand, bid in (line.split() for line in s.splitlines())
            ]
        )


def part1(input: str):
    game = Game.from_str(input)
    hands = sorted(game.hands)
    return sum(hand.bid * (i + 1) for i, hand in enumerate(hands))


def part2(input: str):
    pass


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 6440)
        self.assertEqual(part1(self.input), 247815719)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

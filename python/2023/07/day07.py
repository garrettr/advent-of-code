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
    jokers_wild: bool = False

    CARD_LABELS = "23456789TJQKA"
    CARD_LABELS_JOKERS_WILD = "J" + CARD_LABELS.replace("J", "")

    @property
    def type(self) -> Type:
        assert len(self.hand) == 5
        counter = Counter(self.hand)

        if self.jokers_wild and (num_jokers := counter["J"]) > 0:
            del counter["J"]
            if num_jokers == 5:
                counter["A"] = num_jokers
            else:
                counter[counter.most_common(1)[0][0]] += num_jokers

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
                labels = (
                    self.CARD_LABELS_JOKERS_WILD
                    if self.jokers_wild
                    else self.CARD_LABELS
                )
                for self_card, other_card in zip(self.hand, other.hand):
                    if self_card != other_card:
                        return labels.index(self_card) < labels.index(other_card)

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
            ],
        )

    def sort_hands_by_strength(self, jokers_wild: bool = False):
        # Gross hack to communicate game metavar to `Hand.type`.
        for hand in self.hands:
            hand.jokers_wild = jokers_wild
        self.hands.sort()


def part1(input: str):
    game = Game.from_str(input)
    game.sort_hands_by_strength()
    return sum(hand.bid * (i + 1) for i, hand in enumerate(game.hands))


def part2(input: str):
    game = Game.from_str(input)
    game.sort_hands_by_strength(jokers_wild=True)
    return sum(hand.bid * (i + 1) for i, hand in enumerate(game.hands))


class TestDay(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 6440)
        self.assertEqual(part1(self.input), 247815719)

    def test_part2(self):
        self.assertEqual(part2(self.example), 5905)
        self.assertEqual(part2(self.input), 248747492)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
from enum import Enum

from advent import get_puzzle_input


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def from_char(cls, c):
        if c == "A":
            return cls.ROCK
        elif c == "B":
            return cls.PAPER
        elif c == "C":
            return cls.SCISSORS
        raise ValueError


class Outcome(Enum):
    WIN = 6
    LOSE = 0
    DRAW = 3

    @classmethod
    def from_char(cls, c):
        if c == "X":
            return cls.LOSE
        elif c == "Y":
            return cls.DRAW
        elif c == "Z":
            return cls.WIN


BEATEN_BY = {
    Hand.ROCK: Hand.SCISSORS,
    Hand.PAPER: Hand.ROCK,
    Hand.SCISSORS: Hand.PAPER,
}

BEATS = {v: k for (k, v) in BEATEN_BY.items()}


def score_round(opp_hand, outcome):
    if outcome is Outcome.DRAW:
        hand = opp_hand
    elif outcome is Outcome.WIN:
        hand = BEATS[opp_hand]
    elif outcome is Outcome.LOSE:
        hand = BEATEN_BY[opp_hand]

    return outcome.value + hand.value


def main():
    total_score = 0
    for line in get_puzzle_input(2022, 2).splitlines():
        chars = line.strip().split()
        opponent = Hand.from_char(chars[0])
        outcome = Outcome.from_char(chars[1])
        total_score += score_round(opponent, outcome)
    print(total_score)


if __name__ == "__main__":
    main()

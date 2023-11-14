#!/usr/bin/env python3
from enum import Enum


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


def score_round(opponent, outcome):
    if outcome is Outcome.DRAW:
        hand = opponent
    elif outcome is Outcome.WIN:
        if opponent is Hand.ROCK:
            hand = Hand.PAPER
        elif opponent is Hand.PAPER:
            hand = Hand.SCISSORS
        elif opponent is Hand.SCISSORS:
            hand = Hand.ROCK
        else:
            raise ValueError
    elif outcome is Outcome.LOSE:
        if opponent is Hand.ROCK:
            hand = Hand.SCISSORS
        elif opponent is Hand.PAPER:
            hand = Hand.ROCK
        elif opponent is Hand.SCISSORS:
            hand = Hand.PAPER
        else:
            raise ValueError
    else:
        raise ValueError

    return outcome.value + hand.value


def main():
    total_score = 0

    with open("input.txt") as f:
        for line in f:
            chars = line.strip().split()
            opponent = Hand.from_char(chars[0])
            outcome = Outcome.from_char(chars[1])
            total_score += score_round(opponent, outcome)

    print(total_score)


if __name__ == "__main__":
    main()

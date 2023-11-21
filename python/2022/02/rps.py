#!/usr/bin/env python3
from enum import Enum


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def from_str(cls, s):
        if s == "A" or s == "X":
            return cls.ROCK
        elif s == "B" or s == "Y":
            return cls.PAPER
        elif s == "C" or s == "Z":
            return cls.SCISSORS
        raise ValueError


def score_round(opp, you):
    score = you.value
    if opp == you:  # Draw
        score += 3
    elif (  # You win
        (you == Hand.ROCK and opp == Hand.SCISSORS)
        or (you == Hand.SCISSORS and opp == Hand.PAPER)
        or (you == Hand.PAPER and opp == Hand.ROCK)
    ):
        score += 6
    return score


def main():
    total_score = 0

    with open("input.txt") as f:
        for line in f:
            opp, you = [Hand.from_str(c) for c in line.strip().split()]
            total_score += score_round(opp, you)

    print(total_score)


if __name__ == "__main__":
    main()

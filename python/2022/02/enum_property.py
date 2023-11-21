#!/usr/bin/env python3
"""
https://www.youtube.com/watch?v=Tbm4ycpq2ic
wasn't sure if Enums could have @properties, so I wrote a quick test to see. They can!
"""
from enum import Enum


class Shape(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    @property
    def score(self):
        if self is Shape.ROCK:
            return 1
        elif self is Shape.PAPER:
            return 2
        elif self is Shape.SCISSORS:
            return 3

r = Shape.ROCK
print(r.score)
p = Shape.PAPER
print(p.score)
s = Shape.SCISSORS
print(s.score)

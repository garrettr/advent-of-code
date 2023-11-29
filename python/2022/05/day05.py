#!/usr/bin/env python3
from collections import namedtuple
import os
import sys

from advent import get_puzzle_input

Move = namedtuple("Move", "count src dst")


class Moves(list):
    @classmethod
    def from_str(cls, str):
        lines = str.strip().split("\n")
        moves = [
            Move._make([int(s) for s in line.split() if s.isnumeric()])
            for line in lines
        ]
        return cls(moves)


class Crates:
    def __init__(self, crates):
        self.crates = crates

    @classmethod
    def from_str(cls, str):
        lines = str.split("\n")

        num_stacks = int(lines[-1].split()[-1])
        crates = [[] for i in range(num_stacks)]

        for line in lines[-2::-1]:
            cols = [line[i] for i in range(1, len(line), 4)]
            for i, col in enumerate(cols):
                if col != " ":
                    crates[i].append(col)

        return cls(crates)

    def rearrange(self, moves, crane_model_no="9000"):
        for move in moves:
            for i in range(move.count):
                if crane_model_no == "9000":
                    self.crates[move.dst - 1].append(self.crates[move.src - 1].pop())
                elif crane_model_no == "9001":
                    self.crates[move.dst - 1].append(
                        self.crates[move.src - 1].pop(-1 * (move.count - i))
                    )

    @property
    def tops(self):
        return [stack[-1] for stack in self.crates]


def part1(crates, moves):
    crates.rearrange(moves)
    return "".join(crates.tops)


def part2(crates, moves):
    crates.rearrange(moves, crane_model_no="9001")
    return "".join(crates.tops)


# if __name__ == "__main__":
#     input_path = (
#         sys.argv[1]
#         if len(sys.argv) > 1
#         else os.path.join(os.path.dirname(__file__), "input.txt")
#     )
#     with open(input_path) as input_file:
#         crates_desc, moves_desc = input_file.read().split("\n\n")
#         moves = Moves.from_str(moves_desc)
#         crates = Crates.from_str(crates_desc)
#         print(part1(crates, moves))
#         crates = Crates.from_str(crates_desc)
#         print(part2(crates, moves))

crates_desc, moves_desc = get_puzzle_input(2022, 5).split("\n\n")
moves = Moves.from_str(moves_desc)
crates = Crates.from_str(crates_desc)
print(part1(crates, moves))
crates = Crates.from_str(crates_desc)
print(part2(crates, moves))

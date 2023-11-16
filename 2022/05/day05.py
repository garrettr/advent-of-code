#!/usr/bin/env python3
import os
import sys


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

    def rearrange(self, moves_desc):
        moves = moves_desc.strip().split("\n")

        for move in moves:
            count, src, dst = [int(s) for s in move.split() if s.isnumeric()]
            # print(count, src, dst)
            for i in range(count):
                self.crates[dst - 1].append(self.crates[src - 1].pop())
                # print(self.crates)

    @property
    def tops(self):
        return [stack[-1] for stack in self.crates]


def part1(input_file):
    crates_desc, moves_desc = input_file.read().split("\n\n")
    crates = Crates.from_str(crates_desc)
    # print(crates.crates)
    crates.rearrange(moves_desc)
    # print(crates.crates)
    return "".join(crates.tops)


if __name__ == "__main__":
    input_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(os.path.dirname(__file__), "input.txt")
    )
    with open(input_path) as input_file:
        print(part1(input_file))

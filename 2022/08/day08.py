#!/usr/bin/env python3
from pprint import pprint


TEST = """30373
25512
65332
33549
35390"""


class Map:
    def __init__(self, trees):
        self.trees = trees
        self.rows = len(trees)
        self.cols = len(trees[0])
        self.visibilities = [
            [set() for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.compute_visibilities()

    @classmethod
    def from_string(cls, map):
        return cls([[int(h) for h in line] for line in map.splitlines()])

    def __str__(self):
        return "\n".join("".join(str(h) for h in line) for line in self.trees)

    def compute_visibilities(self):
        # From the left
        for r in range(self.rows):
            for c in range(self.cols):
                if c == 0 or self.trees[r][c] > max(t for t in self.trees[r][:c]):
                    self.visibilities[r][c].add("L")

        # From the right
        for r in range(self.rows):
            for c in reversed(range(self.cols)):
                if c == self.cols - 1 or self.trees[r][c] > max(
                    t for t in self.trees[r][c + 1 :]
                ):
                    self.visibilities[r][c].add("R")

        # From the top
        for c in range(self.cols):
            for r in range(self.rows):
                if r == 0 or self.trees[r][c] > max(
                    t for t in [self.trees[i][c] for i in range(r)]
                ):
                    self.visibilities[r][c].add("T")

        # From the bottom
        for c in range(self.cols):
            for r in reversed(range(self.rows)):
                if r == self.rows - 1 or self.trees[r][c] > max(
                    t for t in [self.trees[i][c] for i in range(r + 1, self.rows)]
                ):
                    self.visibilities[r][c].add("B")

    @property
    def visible(self) -> int:
        return sum(1 for row in self.visibilities for tree in row if tree)

    @property
    def invisible(self) -> int:
        return sum(1 for row in self.visibilities for tree in row if not tree)


def test():
    m = Map.from_string(TEST)
    pprint(m.trees)
    pprint(m.visibilities)
    assert m.visible == 21


def part1(s):
    m = Map.from_string(s)
    print(m.visible)


with open("input.txt") as f:
    s = f.read().strip()
    part1(s)

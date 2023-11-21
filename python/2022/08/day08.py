#!/usr/bin/env python3
import os
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

        self.scenic_scores = [[0] * self.cols for _ in range(self.rows)]
        self.compute_scenic_scores()

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

    def compute_scenic_scores(self):
        for r in range(self.rows):
            for c in range(self.cols):
                tree = self.trees[r][c]

                # Looking up
                up = 0
                for i in reversed(range(r)):
                    up += 1
                    if self.trees[i][c] >= tree:
                        break

                # Looking down
                down = 0
                for i in range(r + 1, self.rows):
                    down += 1
                    if self.trees[i][c] >= tree:
                        break

                # Looking left
                left = 0
                for i in reversed(range(c)):
                    left += 1
                    if self.trees[r][i] >= tree:
                        break

                # Looking right
                right = 0
                for i in range(c + 1, self.cols):
                    right += 1
                    if self.trees[r][i] >= tree:
                        break

                self.scenic_scores[r][c] = up * down * left * right

    @property
    def visible(self) -> int:
        return sum(1 for row in self.visibilities for tree in row if tree)

    @property
    def invisible(self) -> int:
        return sum(1 for row in self.visibilities for tree in row if not tree)

    @property
    def highest_scenic_score(self) -> int:
        return max(max(row) for row in self.scenic_scores)


def test():
    m = Map.from_string(TEST)
    pprint(m.trees)
    pprint(m.visibilities)
    assert m.visible == 21
    assert m.highest_scenic_score == 8


input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path) as f:
    input = f.read().strip()
    m = Map.from_string(input)
    # Part 1
    print(m.visible)
    # Part 2
    print(m.highest_scenic_score)

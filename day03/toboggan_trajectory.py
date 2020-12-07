#!/usr/bin/env python3
from functools import reduce
from itertools import accumulate
import operator

class Map:
    TREE = '#'
    
    def __init__(self, grid):
        self.grid = grid

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            grid = [list(line) for line in lines]
            return cls(grid)

    def trees_for_slope(self, right, down):
        x, y = 0, 0
        # We've reached the bottom when we go past the bottom of the map.
        bottom = len(self.grid)
        trees = 0
        
        while y < bottom:
            if self.grid[y][x] == self.TREE:
                trees += 1

            x = (x + right) % len(self.grid[x])
            y += down

        return trees


def part1(map):
    return map.trees_for_slope(3, 1)

    
def part2(map):
    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    trees = (map.trees_for_slope(*slope) for slope in slopes)
    return reduce(operator.mul, trees)

    
def main():
    map = Map.from_file('input.txt')
    print(part1(map))
    print(part2(map))


if __name__ == '__main__':
    main()

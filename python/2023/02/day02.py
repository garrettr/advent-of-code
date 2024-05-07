#!/usr/bin/env python3
from functools import reduce
from operator import mul
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 2

Game = dict[str, int]

def parse(input: str) -> list[Game]:
    games = []
    for line in input.splitlines():
        game: Game = {}
        handfuls = line.split(": ")[1].split("; ")
        for handful in handfuls:
            for pick in handful.split(", "):
                n, color = pick.split()
                count = int(n)
                if color not in game or game[color] < count:
                    game[color] = count
        games.append(game)
    return games


def is_game_possible(game: Game, totals: Game) -> bool:
    return all(totals.get(color, 0) >= n for color, n in game.items())


def part1(input: str) -> int:
    games = parse(input)
    totals = {"red": 12, "green": 13, "blue": 14}
    return sum(i + 1 for i, game in enumerate(games) if is_game_possible(game, totals))


def part2(input: str) -> int:
    games = parse(input)
    return sum(reduce(mul, game.values()) for game in games)


class TestDay02(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 8)
        self.assertEqual(part1(self.input), 2149)

    def test_part2(self):
        self.assertEqual(part2(self.example), 2286)
        self.assertEqual(part2(self.input), 71274)

        
if __name__ == "__main__":
    unittest.main()

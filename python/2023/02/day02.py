from functools import reduce
from operator import mul
from pprint import pprint

from advent import get_puzzle_input


def parse(input: str):
    games = []
    for line in input.splitlines():
        game = {}
        handfuls = line.split(": ")[1].split("; ")
        for handful in handfuls:
            for pick in handful.split(", "):
                n, color = pick.split()
                n = int(n)
                if (color not in game) or (color in game and game[color] < n):
                    game[color] = n
        games.append(game)
    return games


def is_game_possible(game, totals):
    for color, n in game.items():
        if color not in totals or totals[color] < n:
            return False
    return True


def part1(input: str):
    games = parse(input)
    totals = {"red": 12, "green": 13, "blue": 14}
    return sum(
        [i + 1 for i, game in enumerate(games) if is_game_possible(game, totals)]
    )


def part2(input: str):
    games = parse(input)
    return sum([reduce(mul, game.values()) for game in games])


if __name__ == "__main__":
    example = get_puzzle_input(2023, 2, "example.txt")
    input = get_puzzle_input(2023, 2)

    print(part1(input))
    print(part2(input))

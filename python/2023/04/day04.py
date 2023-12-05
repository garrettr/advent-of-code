from dataclasses import dataclass
from pprint import pprint

from advent import get_puzzle_input


@dataclass
class ScratchCard:
    winning_numbers: set[int]
    numbers_you_have: set[int]

    @classmethod
    def from_str(cls, s: str):
        number_lists = s.split(":")[1].strip().split("|")
        numbers = [
            {int(n) for n in number_list.split()} for number_list in number_lists
        ]
        return cls(*numbers)

    def score(self) -> int:
        intersection = self.winning_numbers & self.numbers_you_have
        return 2 ** (len(intersection) - 1) if intersection else 0


def parse_cards(input: str) -> list[ScratchCard]:
    return [ScratchCard.from_str(line) for line in input.splitlines()]


def part1(input: str):
    return sum(card.score() for card in parse_cards(input))


def part2(input: str):
    pass


if __name__ == "__main__":
    example = get_puzzle_input(2023, 4, "example.txt")
    input = get_puzzle_input(2023, 4)
    print(part1(input))
    # print(part2(input))

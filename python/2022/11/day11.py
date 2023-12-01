#!/usr/bin/env python3
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import NamedTuple

from advent import get_puzzle_input


class Test(NamedTuple):
    cond: int
    conseq: int
    alt: int


@dataclass
class Monkey:
    items: list[int]
    operation: str
    test: Test
    inspections: int = 0

    @classmethod
    def from_str(cls, s: str):
        lines = s.splitlines()
        items = [int(item) for item in lines[1].split(": ")[1].split(", ")]
        operation = lines[2].split(" = ")[1]
        test = Test(*[int(line.split()[-1]) for line in lines[3:]])
        return cls(items, operation, test)

    def __str__(self):
        return "\n".join(
            [
                f"Items: {self.items}",
                f"Operation: {self.operation}",
                f"Test: {self.test}",
                f"Inspections: {self.inspections}",
            ]
        )


def parse(input: str) -> list[Monkey]:
    monkey_descs = input.split("\n\n")
    return [Monkey.from_str(desc) for desc in monkey_descs]


def monkeysstr(monkeys: list[Monkey]):
    return "\n\n".join([f"Monkey {i}:\n{monkey}" for i, monkey in enumerate(monkeys)])


def simulate_monkey_business(monkeys, rounds=1, verbose=False):
    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            if verbose:
                print(f"Monkey {i}:")

            thrown = []

            for j, item in enumerate(monkey.items):
                if verbose:
                    print(f"  Monkey inspects an item with a worry level of {item}")

                old = item
                item = eval(monkey.operation)
                if verbose:
                    print(f"    Worry level is modified to {item}")

                item //= 3
                if verbose:
                    print(
                        f"    Monkey gets bored with item. Worry level is divided by 3 to {item}."
                    )

                if item % monkey.test.cond == 0:
                    thrown.append((j, item, monkey.test.conseq))
                    if verbose:
                        print(
                            f"    Current worry level is divisible by {monkey.test.cond}"
                        )
                else:
                    thrown.append((j, item, monkey.test.alt))
                    if verbose:
                        print(
                            f"    Current worry level is not divisible by {monkey.test.cond}"
                        )

                monkey.inspections += 1

            for j, (src, item, dst) in enumerate(thrown):
                monkey.items.pop(src - j)
                monkeys[dst].items.append(item)
                if verbose:
                    print(
                        f"    Item with worry level {item} is thrown to monkey {dst}."
                    )

    return monkeys


def part1(input):
    monkeys = parse(input)
    simulate_monkey_business(monkeys, 20)
    return reduce(mul, sorted([monkey.inspections for monkey in monkeys])[-2:])


if __name__ == "__main__":
    input = get_puzzle_input(2022, 11)
    print(part1(input))

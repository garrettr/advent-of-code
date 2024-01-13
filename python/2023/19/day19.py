#!/usr/bin/env python3
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from pprint import pprint
import unittest

from advent import get_puzzle_input

YEAR = 2023
DAY = 19


@dataclass
class Part:
    ratings: dict[str, int]

    @classmethod
    def from_str(cls, s: str):
        return Part(
            {
                category: int(rating)
                for category, rating in (
                    part.split("=") for part in s.strip("{}").split(",")
                )
            }
        )

    @property
    def total(self) -> int:
        return sum(rating for rating in self.ratings.values())


class Result(Enum):
    ACCEPT = auto()
    REJECT = auto()


@dataclass
class Rule:
    condition: str | None
    consequent: str | Result

    @classmethod
    def from_str(cls, s: str):
        condition = None
        consequent = None

        if ":" in s:
            condition, s = s.split(":")

        if s == "A":
            consequent = Result.ACCEPT
        elif s == "R":
            consequent = Result.REJECT
        else:
            consequent = s

        return cls(condition, consequent)


@dataclass
class Workflow:
    name: str
    rules: list[Rule]

    @classmethod
    def from_str(cls, s: str):
        name, rules = s.split("{")
        rules = [Rule.from_str(rule) for rule in rules.strip("}").split(",")]
        return cls(name, rules)


def parse(input: str) -> (list[Workflow], list[Part]):
    workflows, parts = input.strip().split("\n\n")
    workflows = [Workflow.from_str(line) for line in workflows.splitlines()]
    parts = [Part.from_str(line) for line in parts.splitlines()]
    return workflows, parts


def part1(input: str) -> int:
    workflows, parts = parse(input)
    workflows = {workflow.name: workflow for workflow in workflows}
    results = defaultdict(list)

    for part in parts:
        workflow = workflows["in"]
        while workflow:
            for rule in workflow.rules:
                if not rule.condition or (
                    rule.condition and eval(rule.condition, globals(), part.ratings)
                ):
                    consequent = rule.consequent
                    if isinstance(consequent, str):
                        workflow = workflows[consequent]
                    else:
                        results[consequent].append(part)
                        workflow = None
                    break

    return sum(part.total for part in results[Result.ACCEPT])


def part2(input: str):
    pass


class TestDay19(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(YEAR, DAY, "example.txt")
        self.input = get_puzzle_input(YEAR, DAY)

    def test_part1(self):
        self.assertEqual(part1(self.example), 19114)
        self.assertEqual(part1(self.input), 362930)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), None)
    #     self.assertEqual(part2(self.input), None)


if __name__ == "__main__":
    unittest.main()

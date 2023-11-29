#!/usr/bin/env python3
from advent import get_puzzle_input


def fully_contained(pair):
    a, b = pair
    return (a[0] <= b[0] and a[1] >= b[1]) or (b[0] <= a[0] and b[1] >= a[1])


def overlapping(pair):
    a, b = pair
    larger, smaller = (a, b) if a[1] - a[0] > b[1] - b[0] else (b, a)
    larger_range = range(larger[0], larger[1] + 1)
    return smaller[0] in larger_range or smaller[1] in larger_range


def parse(string):
    pairs = []
    for line in string.splitlines():
        pair = []
        assignments = line.strip().split(",")
        for assignment in assignments:
            assignment = [int(n) for n in assignment.split("-")]
            pair.append(assignment)
        pairs.append(pair)
    return pairs


def part1(pairs):
    return sum([fully_contained(pair) for pair in pairs])


def part2(pairs):
    return sum([overlapping(pair) for pair in pairs])


pairs = parse(get_puzzle_input(2022, 4))
print(part1(pairs))
print(part2(pairs))

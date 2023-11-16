#!/usr/bin/env python3


def fully_contained(pair):
    a, b = pair
    return (a[0] <= b[0] and a[1] >= b[1]) or (b[0] <= a[0] and b[1] >= a[1])


def parse(file):
    pairs = []
    for line in file:
        pair = []
        assignments = line.strip().split(",")
        for assignment in assignments:
            assignment = [int(n) for n in assignment.split("-")]
            pair.append(assignment)
        pairs.append(pair)
    return pairs


def part1(file):
    pairs = parse(file)
    fully_contained_pairs_count = 0
    for pair in pairs:
        if fully_contained(pair):
            fully_contained_pairs_count += 1
    return fully_contained_pairs_count


if __name__ == "__main__":
    with open("input.txt") as file:
        print(part1(file))

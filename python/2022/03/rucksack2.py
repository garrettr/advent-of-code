#!/usr/bin/env python3.12
from itertools import batched


def priority(c):
    if c.isupper():
        return ord(c) - 38
    elif c.islower():
        return ord(c) - 96


def main():
    priorities_sum = 0

    with open("input.txt") as f:
        for group in batched(f.readlines(), 3):
            rucksacks = [set(rucksack.strip()) for rucksack in group]
            intersection = rucksacks.pop().intersection(*rucksacks)
            priorities_sum += priority(intersection.pop())

    print(priorities_sum)


if __name__ == "__main__":
    main()

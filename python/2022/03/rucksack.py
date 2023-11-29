#!/usr/bin/env python3
from advent import get_puzzle_input


def priority(c):
    if c.isupper():
        return ord(c) - 38
    elif c.islower():
        return ord(c) - 96


def main():
    priorities_sum = 0

    for line in get_puzzle_input(2022, 3).splitlines():
        ruck_desc = line.strip()
        mid = len(ruck_desc) // 2
        c1 = set(ruck_desc[:mid])
        c2 = set(ruck_desc[mid:])
        shared = c1.intersection(c2)
        priorities_sum += priority(shared.pop())

    print(priorities_sum)


if __name__ == "__main__":
    main()

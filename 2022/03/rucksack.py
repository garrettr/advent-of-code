#!/usr/bin/env python3


def priority(c):
    if c.isupper():
        return ord(c) - 38
    elif c.islower():
        return ord(c) - 96


def main():
    priorities_sum = 0

    with open("input.txt") as f:
        for line in f:
            ruck_desc = line.strip()
            mid = len(ruck_desc) // 2
            c1 = set(ruck_desc[:mid])
            c2 = set(ruck_desc[mid:])
            shared = c1.intersection(c2)
            priorities_sum += priority(shared.pop())

    print(priorities_sum)


if __name__ == "__main__":
    main()

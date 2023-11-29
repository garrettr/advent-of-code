#!/usr/bin/env python3
from collections import deque

from advent import get_puzzle_input


def part1(datastream, marker_len=4):
    sliding_window = deque(maxlen=marker_len)
    for i, c in enumerate(datastream):
        sliding_window.append(c)
        if i > 2 and len(set(sliding_window)) == marker_len:
            return i + 1


def part2(datastream):
    return part1(datastream, 14)


input = get_puzzle_input(2022, 6)
for line in input.splitlines():
    datastream = line.strip()
    print(part1(datastream))
    print(part2(datastream))

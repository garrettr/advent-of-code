#!/usr/bin/env python3
from collections import deque
import os
import sys


def part1(datastream, marker_len=4):
    sliding_window = deque(maxlen=marker_len)
    for i, c in enumerate(datastream):
        sliding_window.append(c)
        if i > 2 and len(set(sliding_window)) == marker_len:
            return i + 1


def part2(datastream):
    return part1(datastream, 14)


if __name__ == "__main__":
    input_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(os.path.dirname(__file__), "input.txt")
    )
    with open(input_path) as input_file:
        for line in input_file:
            datastream = line.strip()
            print(part1(datastream))
            print(part2(datastream))

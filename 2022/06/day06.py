#!/usr/bin/env python3
from collections import deque
import os
import sys


def part1(datastream):
    last4 = deque(maxlen=4)
    for i, c in enumerate(datastream):
        last4.append(c)
        if i > 2 and len(set(last4)) == 4:
            return i + 1


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

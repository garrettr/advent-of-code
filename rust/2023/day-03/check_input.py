#!/usr/bin/env python3
from collections import Counter
import re


EXAMPLE = "./src/example.txt"
INPUT = "./src/input.txt"

numbers = Counter()

with open(INPUT) as f:
    lines = f.read().splitlines()
    for line in lines:
        for number in (int(num) for num in re.findall(r'[0-9]+', line)):
            numbers[number] += 1

print(numbers)

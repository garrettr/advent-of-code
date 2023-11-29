#!/usr/bin/env python3
from advent import get_puzzle_input


# Each elf is represented by the sum of the calories they're carrying.
elves = []
elf = 0
for line in get_puzzle_input(2022, 1).splitlines():
    if line == "":
        elves.append(elf)
        elf = 0
    else:
        elf += int(line.strip())

elves.sort(reverse=True)
# Part One
print(elves[0])
# Part Two
print(sum(elves[:3]))

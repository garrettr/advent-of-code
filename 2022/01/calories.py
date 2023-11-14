#!/usr/bin/env python3

def main():
    elves = []
    
    # Each elf is represented by the sum of the calories they're carrying.
    elf = 0

    with open("input.txt") as f:
        for line in f:
            if line == '\n':
                elves.append(elf)
                elf = 0
            else:
                elf += int(line.strip())

    elves.sort()
    print(elves[-1])


if __name__ == "__main__":
    main()
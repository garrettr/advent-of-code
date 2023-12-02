from advent import get_puzzle_input


def part1(input):
    ns = []
    for line in input.splitlines():
        ds = [c for c in line if c.isdigit()]
        ns.append(int(ds[0] + ds[-1]))
    return sum(ns)


def part2(input):
    DIGITS = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    digits = list(DIGITS.keys()) + [str(v) for v in DIGITS.values()]
    ns = []
    for line in input.splitlines():
        ds = []

        for i in range(len(line)):
            found = False
            for digit in digits:
                if line[i:].startswith(digit):
                    found = True
                    ds.append(digit)
                    break
            if found:
                break

        for i in range(len(line) - 1, -1, -1):
            found = False
            for digit in digits:
                if line[i:].startswith(digit):
                    found = True
                    ds.append(digit)
                    break
            if found:
                break

        norm_ds = []
        for d in ds:
            if d in DIGITS:
                norm_ds.append(str(DIGITS[d]))
            else:
                norm_ds.append(d)

        ns.append(int("".join(norm_ds)))

    return sum(ns)


if __name__ == "__main__":
    example = get_puzzle_input(2023, 1, "example.txt")
    example2 = get_puzzle_input(2023, 1, "example2.txt")
    input = get_puzzle_input(2023, 1)

    print(part1(input))
    print(part2(input))

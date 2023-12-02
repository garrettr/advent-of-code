from advent import get_puzzle_input


def calibration_value(line: str) -> int:
    digits = [c for c in line if c.isdigit()]
    return int(digits[0] + digits[-1])


def part1(input):
    return sum(calibration_value(line) for line in input.splitlines())


def calibration_value2(line: str) -> int:
    SPELLED_DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    DIGITS = SPELLED_DIGITS + [str(i+1) for i in range(len(SPELLED_DIGITS))]

    first = last = None
    for i in range(len(line)):
        if first and last:
            break

        for digit in DIGITS:
            if not first and line[i:].startswith(digit):
                first = digit
            if not last and line[len(line) - i - 1:].startswith(digit):
                last = digit

    def digit_value(digit):
        if digit in SPELLED_DIGITS:
            return SPELLED_DIGITS.index(digit) + 1
        return int(digit)

    return 10 * digit_value(first) + digit_value(last)


def part2(input):
    return sum(calibration_value2(line) for line in input.splitlines())


if __name__ == "__main__":
    example = get_puzzle_input(2023, 1, "example.txt")
    example2 = get_puzzle_input(2023, 1, "example2.txt")
    input = get_puzzle_input(2023, 1)

    print(part1(input))
    print(part2(input))

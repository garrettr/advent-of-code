from advent import get_puzzle_input


def find_overlapping_part(row: str, col: int) -> int:
    start = end = None
    for i in range(col, -1, -1):
        if not row[i].isdigit():
            start = i + 1
            break
    for i in range(col, len(row)):
        if not row[i].isdigit():
            end = i
            break
    return int(row[start:end])


def find_surrounding_parts(input: str, row: int, col: int) -> list[int]:
    rows = input.splitlines()
    parts = []
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if r == row and c == col:
                continue
            if r < 0 or c < 0:
                continue
            try:
                if rows[r][c].isdigit():
                    parts.append(find_overlapping_part(rows[r], c))
            except IndexError:
                continue
    return list(set(parts))


def parse_engine_schematic(input: str):
    parts = []
    for row, line in enumerate(input.splitlines()):
        for col, char in enumerate(line):
            if char != "." and not char.isdigit():
                parts.extend(find_surrounding_parts(input, row, col))
    return parts


def part1(input: str):
    parts = parse_engine_schematic(input)
    return sum(parts)


def part2(input: str):
    pass


if __name__ == "__main__":
    example = get_puzzle_input(2023, 3, "example.txt")
    input = get_puzzle_input(2023, 3)

    print(part1(input))

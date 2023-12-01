#!/usr/bin/env python3
import argparse
import sys
from datetime import date

from .puzzle import challenges_path, challenge_path
from .website import download_puzzle_input


def get_current_puzzle() -> (int, int):
    """Get the year and day of the most recently published Advent of Code puzzle."""
    today = date.today()
    year = today.year - (0 if today.month == 12 else 1)
    day = min(today.day, 25) if today.month == 12 else 25
    return (year, day)


def do_language_specific_setup(language: str, year: int, day: int, path):
    match language:
        case "python":
            # TODO: Copy template .py
            pass


def new(language: str, year: int, day: int):
    """Prepare for a new day's challenge."""
    path = challenges_path(language)
    if not path.exists():
        res = input(f"Challenges directory {path} does not exist, create it? (y/n) ")
        if res.lower() == "y":
            path.mkdir(parents=True)
        else:
            return

    path = challenge_path(language, year, day)
    if path.exists():
        res = input(f"Challenge directory {path} already exists, replace it? (y/n) ")
        if res.lower() == "y":
            path.rmdir()
        else:
            return
    path.mkdir(parents=True)

    puzzle_input = download_puzzle_input(year, day)
    with open(path / "input.txt", "w") as f:
        f.write(puzzle_input)

    do_language_specific_setup(language, year, day, path)


def main():
    parser = argparse.ArgumentParser(description="Advent of Code helper tool")
    subparsers = parser.add_subparsers(
        dest="subcommand",
        title="subcommands",
    )

    new_cmd = subparsers.add_parser("new", help="Prepare for a new day's challenge")
    new_cmd.add_argument(
        "language",
        choices=["python"],
        nargs="?",
        default="python",
        help="Language to use",
    )
    (year, day) = get_current_puzzle()
    new_cmd.add_argument(
        "year", type=int, nargs="?", default=year, help="Year the puzzle was published"
    )
    new_cmd.add_argument(
        "day", type=int, nargs="?", default=day, help="Day the puzzle was published"
    )

    args = parser.parse_args()

    try:
        match args.subcommand:
            case "new":
                new(args.language, args.year, args.day)
    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

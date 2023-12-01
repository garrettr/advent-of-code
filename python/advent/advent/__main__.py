#!/usr/bin/env python3
import argparse
import sys

from .puzzle import challenges_path, challenge_path
from .website import download_puzzle_input


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
    new_cmd.add_argument("language", choices=["python"], help="Language to use")
    new_cmd.add_argument("year", type=int, help="Year of the day to create")
    new_cmd.add_argument("day", type=int, help="Day to create")

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


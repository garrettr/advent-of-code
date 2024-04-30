#!/usr/bin/env python3
import argparse
import sys
from datetime import date

from .puzzle import Puzzle, Language


def get_latest_puzzle() -> tuple[int, int]:
    """Get the year and day of the latest Advent of Code puzzle."""
    today = date.today()
    year = today.year - (0 if today.month == 12 else 1)
    day = min(today.day, 25) if today.month == 12 else 25
    return year, day


def main():
    parser = argparse.ArgumentParser(description="Advent of Code helper tool")
    subparsers = parser.add_subparsers(
        dest="subcommand",
        title="subcommands",
    )

    new_cmd = subparsers.add_parser("new", help="Prepare for a new day's puzzle")
    new_cmd.add_argument(
        "language",
        choices=[str(language) for language in Language],
        nargs="?",
        default="python",
        help="Programming language to use for solution implementation",
    )
    year, day = get_latest_puzzle()
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
                puzzle = Puzzle(args.language, args.year, args.day)
                puzzle.new()
    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

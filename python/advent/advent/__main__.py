#!/usr/bin/env python3
import argparse

from .puzzle import challenges_path, challenge_path


def download_input_files(year, day, path):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    # TODO: Oauth
    pass


def language_specific_setup(language, year, day, path):
    # If Python, copy template file
    pass


def new(language: str, year: int, day: int):
    """Prepare for a new day's challenge."""
    path = challenges_path(language)
    if not path.exists():
        res = input(f"Challenges directory {path} does not exist, create it? (y/n)")
        if res.lower() == "y":
            path.mkdir(parents=True)
        else:
            return

    path = challenge_path(language, year, day)
    if path.exists():
        res = input(f"Challenge directory {path} already exists, replace it? (y/n)")
        if res.lower() == "y":
            path.rmdir()
        else:
            return
    path.mkdir(parents=True)
    print(f"Created challenge directory {path}...")

    download_input_files(year, day, path)
    language_specific_setup(language, year, day, path)


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="Advent of Code helper tool")
    subparsers = parser.add_subparsers(
        dest="subcommand",
        title="subcommands",
    )

    # Create a subparser for the "new" subcommand
    subcmd_new = subparsers.add_parser("new", help="Prepare for a new day's challenge")
    subcmd_new.add_argument("language", choices=["python"], help="Language to use")
    subcmd_new.add_argument("year", type=int, help="Year of the day to create")
    subcmd_new.add_argument("day", type=int, help="Day to create")

    args = parser.parse_args()

    if args.subcommand == "new":
        new(args.language, args.year, args.day)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import shutil
import subprocess
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
            # Create challenge directory.
            path.mkdir(parents=True)

            # Copy template file, substituting the current year and day.
            with open(challenges_path(language) / "template.py") as f:
                template = f.read()
            template = template.replace("YEAR = 2023", f"YEAR = {year}")
            template = template.replace("DAY = 1", f"DAY = {day}")
            solution_src = path / f"day{day:02d}.py"
            with open(solution_src, "w") as f:
                f.write(template)
            solution_src.chmod(0o755)

        case "rust":
            # Create challenge directory and boilerplate binary package with Cargo.
            try:
                subprocess.run(
                    ["cargo", "new", path.name],
                    capture_output=True,
                    check=True,
                    cwd=path.parent,
                )
            except subprocess.CalledProcessError as e:
                print(e.stderr.decode("utf-8"))
                raise

            # Copy template file.
            shutil.copyfile(
                challenges_path(language) / "template.rs", path / "src" / "main.rs"
            )


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

    do_language_specific_setup(language, year, day, path)

    puzzle_input = download_puzzle_input(year, day)
    input_dir = path / "src" if language == "rust" else path
    with open(input_dir / "input.txt", "w") as f:
        f.write(puzzle_input)


def main():
    parser = argparse.ArgumentParser(description="Advent of Code helper tool")
    subparsers = parser.add_subparsers(
        dest="subcommand",
        title="subcommands",
    )

    new_cmd = subparsers.add_parser("new", help="Prepare for a new day's challenge")
    new_cmd.add_argument(
        "language",
        choices=["python", "rust"],
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

#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from datetime import date

from .puzzle import get_challenges_path, get_challenge_path
from .website import download_puzzle_input


def get_current_puzzle() -> tuple[int, int]:
    """Get the year and day of the most recently published Advent of Code puzzle."""
    today = date.today()
    year = today.year - (0 if today.month == 12 else 1)
    day = min(today.day, 25) if today.month == 12 else 25
    return year, day


def setup_python(year: int, day: int, challenge_path: str):
    # Create challenge directory.
    challenge_path.mkdir(parents=True)

    # Copy template file, substituting the current year and day.
    with open(get_challenges_path("python") / "template.py") as f:
        template = f.read()
        template = template.replace("YEAR = 2023", f"YEAR = {year}")
        template = template.replace("DAY = 1", f"DAY = {day}")
        template = template.replace("TestDay", f"TestDay{day}")
        solution_src = challenge_path / f"day{day:02d}.py"
        with open(solution_src, "w") as f:
            f.write(template)
        solution_src.chmod(0o755)


def setup_rust(year: int, day: int, challenge_path: str):
    # Create parent directory (`rust/<year>`).
    try:
        challenge_path.parent.mkdir(parents=True)
    except FileExistsError:
        pass

    # Create challenge directory and boilerplate binary package with Cargo.
    try:
        subprocess.run(
            ["cargo", "new", challenge_path.name],
            capture_output=True,
            check=True,
            cwd=challenge_path.parent,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode("utf-8"))
        raise

    # Copy template file.
    shutil.copyfile(
        get_challenges_path("rust") / "template.rs",
        challenge_path / "src" / "main.rs"
    )


def do_language_specific_setup(language: str, year: int, day: int, challenge_path: str):
    if language == "python":
        setup = setup_python
    elif language == "rust":
        setup = setup_rust
    else:
        raise RuntimeError(f"Unsupported language: {language}")
    setup(year, day, challenge_path)


def new(language: str, year: int, day: int):
    """Prepare for a new day's challenge."""
    challenges_path = get_challenges_path(language)
    if not challenges_path.exists():
        res = input(f"Challenges directory {challenges_path} does not exist, create it? (y/n) ")
        if res.lower() == "y":
            challenges_path.mkdir(parents=True)
        else:
            return

    challenge_path = get_challenge_path(language, year, day)
    if challenge_path.exists():
        res = input(f"Challenge directory {challenge_path} already exists, replace it? (y/n) ")
        if res.lower() == "y":
            shutil.rmtree(challenge_path)
        else:
            return

    do_language_specific_setup(language, year, day, challenge_path)

    if language == "rust":
        input_dir = challenge_path / "src"
    else:
        input_dir = challenge_path
    puzzle_input = download_puzzle_input(year, day)
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

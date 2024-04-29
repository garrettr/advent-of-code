import pathlib
import subprocess


def repo_root():
    """Return the path to the root of the Git repository containing this file."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            check=True,
            cwd=pathlib.Path(__file__).parent,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode("utf-8"))
        raise
    return pathlib.Path(result.stdout.decode("utf-8").strip())


def get_challenges_path(language: str) -> pathlib.Path:
    """Return the path to the subdirectory of solutions to challenges written in `language`."""
    return repo_root() / language


def get_challenge_path(language: str, year: int, day: int):
    """Return the path to the subdirectory containing the solution for a specific challenge."""
    if language == "rust":
        day_dir = f"day-{day:02d}"
    else:
        day_dir = f"{day:02d}"
    return get_challenges_path(language) / str(year) / day_dir


def get_puzzle_input(year: int, day: int, filename="input.txt") -> str:
    """Get the puzzle input for the given year and day."""
    with open(get_challenge_path("python", year, day) / filename) as f:
        return f.read()

from dataclasses import dataclass
from enum import StrEnum, auto
import pathlib
import shutil
import subprocess

from .website import download_puzzle_input


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


def get_puzzles_path_for_language(language: str) -> pathlib.Path:
    """Return the path to the subdirectory of solutions to challenges written in `language`."""
    return repo_root() / language


class Language(StrEnum):
    PYTHON = auto()
    RUST = auto()


@dataclass
class Puzzle:
    "Represents the solution of an Advent of Code puzzle in a programming language."
    language: Language
    year: int
    day: int

    @property
    def path(self):
        "Path to the subdirectory containing the solution for a specific puzzle in a specific language."
        if self.language == Language.RUST:
            day = f"day-{self.day:02d}"
        else:
            day = f"{self.day:02d}"
        return get_puzzles_path_for_language(self.language) / str(self.year) / day

    @property
    def inputs_dir(self):
        """Path to the subdirectory containing puzzle inputs as text files."""
        if self.language == Language.RUST:
            inputs_dir = self.path / "src"
        else:
            inputs_dir = self.path
        return inputs_dir

    INPUT_FILENAME = "input.txt"

    @property
    def input(self, filename=INPUT_FILENAME):
        "Get the contents of a file in the puzzle's inputs directory."
        with open(self.inputs_dir / filename) as f:
            return f.read()

    def _setup_python(self):
        # Create puzzle directory.
        self.path.mkdir(parents=True)

        # Copy template file, substituting the current year and day.
        with open(get_puzzles_path_for_language("python") / "template.py") as f:
            template = f.read()
            template = template.replace("YEAR = 2023", f"YEAR = {self.year}")
            template = template.replace("DAY = 1", f"DAY = {self.day}")
            template = template.replace("TestDay", f"TestDay{self.day}")
            solution_src = self.path / f"day{self.day:02d}.py"
            with open(solution_src, "w") as f:
                f.write(template)
            solution_src.chmod(0o755)

    def _setup_rust(self):
        # Create parent directory (`rust/<year>`).
        try:
            self.path.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        # Create challenge directory and boilerplate binary package with Cargo.
        try:
            subprocess.run(
                ["cargo", "new", self.path.name],
                capture_output=True,
                check=True,
                cwd=self.path.parent,
            )
        except subprocess.CalledProcessError as e:
            print(e.stderr.decode("utf-8"))
            raise

        # Copy template file.
        shutil.copyfile(
            get_puzzles_path_for_language("rust") / "template.rs",
            self.path / "src" / "main.rs"
        )

    def _download_puzzle_input(self):
        puzzle_input = download_puzzle_input(self.year, self.day)
        with open(self.inputs_dir / self.INPUT_FILENAME, "w") as f:
            f.write(puzzle_input)

    def new(self):
        puzzles_path = get_puzzles_path_for_language(self.language)
        if not puzzles_path.exists():
            response = input(f"Puzzles path {puzzles_path} does not exist, create it? (y/n) ")
            if response.lower() == "y":
                puzzles_path.mkdir(parents=True)
            else:
                return

        if self.path.exists():
            response = input(f"Puzzle directory {self.path} already exists, replace it? (y/n) ")
            if response.lower() == "y":
                shutil.rmtree(self.path)

        if self.language == Language.PYTHON:
            self._setup_python()
        elif self.language == Language.RUST:
            self._setup_rust()
        else:
            raise RuntimeError(f"Unsupported language: {self.language}")

        self._download_puzzle_input()
        

def get_puzzle_input(year: int, day: int, filename=Puzzle.INPUT_FILENAME) -> str:
    """Helper function for Python solutions that gets the puzzle input for the given year and day."""
    return Puzzle(language.PYTHON, year, day).input(filename)

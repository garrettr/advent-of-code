import os
import urllib.error
import urllib.request
from functools import cache

import dotenv


dotenv_path = dotenv.find_dotenv(usecwd=True)
dotenv.load_dotenv(dotenv_path)

URL = "https://adventofcode.com/{}/day/{}/input"
SESSION_ID = os.environ.get("SESSION_ID", "")
HEADERS = {
    "User-Agent": "Python",
    "Cookie": f"session={SESSION_ID}",
}


class PuzzleNotFoundError(Exception):
    """Exception raised when a requested Advent of Code puzzle is not found."""


class InvalidSessionIDError(Exception):
    """Exception raised when an invalid session ID is provided."""


def handle_error(error: urllib.error.HTTPError) -> None:
    match error.code:
        case 404:
            raise PuzzleNotFoundError(
                "Puzzle input for the given year and day not found."
            )
        case 400:
            raise InvalidSessionIDError("Session ID has expired or is invalid.")
        case _:
            raise


@cache
def download_puzzle_input(year: int, day: int) -> str:
    req = urllib.request.Request(URL.format(year, day), headers=HEADERS)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        handle_error(err)
    data = response.read().decode()
    return data

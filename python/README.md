# Setup

1. Enter your Python environment of choice (e.g. global, virtualenv, conda). I'm using `venv`:

    ```sh
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    ```

2. Install `advent` as an editable package:

    ```sh
    $ pip install -e ./advent
    ```

3. If using `zsh` without [automatic rehashing](https://superuser.com/questions/1089949/zsh-autocompletion-for-a-fresh-executable-in-path) enabled, run `rehash` so `zsh` picks up the scripts defined by the Python package's `project.scripts` in `pyproject.toml`.

4. Confirm it worked:

    ```sh
    $ python -c "import advent" && echo "OK"
    OK
    $ advent -h
    ```

# Authenticating to the Advent of Code website

To use `advent` commands that interact with the Advent of Code website
you must provide a valid session cookie.

## Obtaining the Session Cookie

1. Navigate to [Advent of Code](https://adventofcode.com) in your web
   browser of choice.
2. Sign in with your OAuth provider of choice.
3. Use your browser's Developer Tools to copy the value of the
   `session` cookie. You only need the value, not the rest of the
   cookie metadata.

## Making the cookie available to `advent`

`advent` looks for the session cookie value in a `SESSION_ID`
environment variable. There are two ways you can set the environment
variable:

1. With your shell. For example, in zsh:

    ```sh
    # Consider taking precautions to prevent your session cookie from being saved in your shell history.
    $ setopt HIST_IGNORE_SPACE
    # Note the extra leading space
    $  export SESSION_ID="<YOUR SESSION ID>"
    ```

2. In a `.env` file.

    ```sh
    $ echo 'SESSION_ID="<YOUR SESSION ID>"' > .env
    ```

`advent` will search for `.env` files by traversing up from the
current working directory. This git repo ignores `.env` files to
prevent accidentally checking in secrets.

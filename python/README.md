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
    $ advent
    Hello from advent __main__.py
    ```
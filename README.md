# Setup

## Python

### `pyenv`

On macOS, install `pyenv` and `pyenv-virtualenv` with Homebrew:
```
brew install pyenv pyenv-virtualenv
```

Install Python 3.12.1:
```
pyenv install -v 3.12.1
```

Create a virtualenv:
```
pyenv virtualenv 3.12.1 advent-of-code
```

`cd` to fresh clone of the `advent-of-code` repository. The
`advent-of-code` virtualenv should be automatically selected due to
the `.python-version` file that I created by running `pyenv local
advent-of-code` in the root of the repository.

### Install the `advent` Python package

We want the `advent` package to work with `pyright`, so we need to be
careful how we setup our editable install. [pyright's Import
Resolution docs][0] suggest two options. We'll use "compat mode" for
now:
```
cd python/advent
pip install -e . --config-settings editable_mode=compat
```

[0]: https://github.com/microsoft/pyright/blob/main/docs/import-resolution.md#editable-installs

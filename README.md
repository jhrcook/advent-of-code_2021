# Advent of Code 2021

**My solutions to the [Advent of Code 2021](https://adventofcode.com/2021) using Python.**

[![advent-of-code](https://img.shields.io/badge/Advent_of_Code-2021-F80046.svg?style=flat)](https://adventofcode.com)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)

| Day | Code                                                                     | Status |
| ----| ------------------------------------------------------------------------ | ------ |
| 1   | [advent_of_code/challenges/day01.py](advent_of_code/challenges/day01.py) | ⭐️⭐️   |
| 2   | [advent_of_code/challenges/day02.py](advent_of_code/challenges/day02.py) | ⭐️⭐️   |
| 3   | [advent_of_code/challenges/day03.py](advent_of_code/challenges/day03.py) | ⭐️⭐️   |
| 4   | [advent_of_code/challenges/day04.py](advent_of_code/challenges/day04.py) | ⭐️⭐️   |

## Details

### Setup

```bash
pyenv local 3.9.9
pyenv exec python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Organization

This repository is actually a Python package with all of the code in the [advent_of_code](./advent_of_code/) directory.
Within there, all of the challenges are in the [advent_of_code/challenges](./advent_of_code/challenges) sub-module where are day has a separate file.
Each of these "day"s can be run by Python to complete the challenge.

### Run all challenges

(TODO)

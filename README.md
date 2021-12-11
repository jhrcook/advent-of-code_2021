# Advent of Code 2021

**My solutions to the [Advent of Code 2021](https://adventofcode.com/2021) using Python.**

[![advent-of-code](https://img.shields.io/badge/Advent_of_Code-2021-F80046.svg?style=flat)](https://adventofcode.com)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)

| Day | Code                                                                     | Status |
| ---:| ------------------------------------------------------------------------ | ------ |
| 1   | [advent_of_code/challenges/day01.py](advent_of_code/challenges/day01.py) | ⭐️⭐️   |
| 2   | [advent_of_code/challenges/day02.py](advent_of_code/challenges/day02.py) | ⭐️⭐️   |
| 3   | [advent_of_code/challenges/day03.py](advent_of_code/challenges/day03.py) | ⭐️⭐️   |
| 4   | [advent_of_code/challenges/day04.py](advent_of_code/challenges/day04.py) | ⭐️⭐️   |
| 5   | [advent_of_code/challenges/day05.py](advent_of_code/challenges/day05.py) | ⭐️⭐️   |
| 6   | [advent_of_code/challenges/day06.py](advent_of_code/challenges/day06.py) | ⭐️⭐️   |
| 7   | [advent_of_code/challenges/day07.py](advent_of_code/challenges/day07.py) | ⭐️⭐️   |
| 8   | [advent_of_code/challenges/day08.py](advent_of_code/challenges/day08.py) | ⭐️⭐️   |
| 9   | [advent_of_code/challenges/day09.py](advent_of_code/challenges/day09.py) | ⭐️⭐️   |
| 10  | [advent_of_code/challenges/day10.py](advent_of_code/challenges/day10.py) | ⭐️⭐️   |
| 11  | [advent_of_code/challenges/day11.py](advent_of_code/challenges/day11.py) | ⭐️⭐️   |

## Details

### Installation

This project can be installed as a Python package using `pip`.
Once it is installed, the code for the challenges can be executed using the CLI command as demonstrated later.

```bash
# pyenv local 3.9.9
python3 -m venv .env # or `pyenv exec python3 -m venv .env`
pip install --upgrade pip
pip install git+https://github.com/jhrcook/advent-of-code_2021.git
```

### Development setup

The steps to setting up the development version of this project are shown below.

```bash
pyenv local 3.9.9
pyenv exec python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install flit
flit install
```

### Run the challenges

It is possible to run the code for a single day's challenge as demonstrated:

```bash
aoc21 --day 1
#> Day 1 part 1 answer: 1226
#> Day 1 part 2 answer: 1252
```

If no day is supplied as input, then the code for all of the challenges is executed in order.

```bash
aoc21
#> Day 1 part 1 answer: 1226
#> Day 1 part 2 answer: 1252
#> Day 2 part 1 answer: 1507611
#> ...
```

Alternatively, if you have the development system setup, you can use [`tox`]https://tox.wiki).

```bash
tox
#> .package recreate: /Users/admin/Developer/Python/advent-of-code_2021/.tox/.package
#> .package installdeps: flit_core >=3.2,<4
#> ...
```

### Organization

This repository is actually a Python package with all of the code in the [advent_of_code](./advent_of_code/) directory.
Within there, all of the challenges are in the [advent_of_code/challenges](./advent_of_code/challenges) sub-module where are day has a separate file.
Each of these "day"s can be run by Python to complete the challenge.

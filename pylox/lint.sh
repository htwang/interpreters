#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $SCRIPT_DIR

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirement-lint.txt > /dev/null

echo "running isort"
python3 -m isort --settings-path ./pyproject.toml .

echo "running black"
python3 -m black --config ./pyproject.toml .

echo "running pyflakes"
python3 -m pyflakes *.py

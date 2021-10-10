#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $SCRIPT_DIR

python3 -m venv .venv
source .venv/bin/activate

pattern=$1

if [[ -z ${pattern} ]]; then
    python3 -m unittest discover -v -p  "*_test.py"
else
    python3 -m unittest discover -v -p  "*_test.py" -k ${pattern}
fi


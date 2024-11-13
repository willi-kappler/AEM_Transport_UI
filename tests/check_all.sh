#!/usr/bin/env bash

reset

export PYTHONPATH=$PYTHONPATH:"src/"

echo "ruff:"
ruff check src/
ruff check tests/

echo -e "\n\n-------------------------------------------\n\n"

echo "mypy:"
mypy --check-untyped-defs src/
mypy --check-untyped-defs tests/


echo -e "\n\n-------------------------------------------\n\n"

echo "flake8:"
flake8 src/
flake8 tests/

echo -e "\n\n-------------------------------------------\n\n"

echo "pyright:"
pyright src/
pyright tests/


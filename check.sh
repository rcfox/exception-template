#!/bin/sh
mypy exception_template tests
pylint exception_template tests

# Tests
python3 exception_template/exception_template.py
python3 -m unittest discover -s tests

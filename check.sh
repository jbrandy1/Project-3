#!/bin/bash

set -e

poetry run black --check *.py
poetry run isort --check *.py
poetry run flake8 *.py



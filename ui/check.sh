#!/bin/bash

set -e

poetry run black --check *.js
poetry run isort --check *.js
poetry run flake8 *.js

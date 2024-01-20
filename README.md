# mkdocs-macros-adr-summary
![Static Badge](https://img.shields.io/badge/Python-3.8_%7C_3.9_%7C_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)
[![Stable Version](https://img.shields.io/pypi/v/mkdocs-macros-adr-summary?color=blue)](https://pypi.org/project/mkdocs-macros-adr-summary/)
[![stability-wip](https://img.shields.io/badge/stability-wip-lightgrey.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#work-in-progress)

[![Python tests](https://github.com/febus982/mkdocs-macros-adr-summary/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/febus982/mkdocs-macros-adr-summary/actions/workflows/python-tests.yml)
[![Bandit checks](https://github.com/febus982/mkdocs-macros-adr-summary/actions/workflows/python-bandit.yml/badge.svg?branch=main)](https://github.com/febus982/mkdocs-macros-adr-summary/actions/workflows/python-bandit.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/5631f62f6dcd3a34d7ae/maintainability)](https://codeclimate.com/github/febus982/mkdocs-macros-adr-summary/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5631f62f6dcd3a34d7ae/test_coverage)](https://codeclimate.com/github/febus982/mkdocs-macros-adr-summary/test_coverage)

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

## Commands for development

All the common commands used during development can be run using make targets:

* `make dev-dependencies`: Install dev requirements
* `make update-dependencies`: Update dev requirements
* `make test`: Run test suite
* `make check`: Run tests, code style and lint checks
* `make fix`: Run code style and lint automatic fixes (where possible)
* `make docs`: Render the mkdocs website locally

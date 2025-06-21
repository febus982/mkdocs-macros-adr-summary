#!/usr/bin/env bash

VERSION=$(uv run scripts/version_from_git.py)
SEMVER=( ${VERSION//./ } )
echo "${SEMVER[0]}.${SEMVER[1]}"

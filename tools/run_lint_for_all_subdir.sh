#!/usr/bin/env bash
# Run linter for all directories under provided directory.
# Good to verify linter on many datasets.

find $1 -name metadata.yaml -exec bash -c 'uv run oellm-package-data -m lint --collection-dir "$(dirname "$1")"' _ {} \;

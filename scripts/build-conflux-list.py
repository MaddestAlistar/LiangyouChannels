#!/usr/bin/env python3
"""Compatibility entry point for the complete ten-section Conflux list."""
from pathlib import Path
from runpy import run_path

implementation = run_path(str(Path(__file__).with_name('build-curated-conflux.py')))
build = implementation['build']

if __name__ == '__main__':
    implementation['main']()

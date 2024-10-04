#!/usr/bin/env python3
"""Create test report directories."""
import os
import shutil
from pathlib import Path

if os.path.exists('reports'):
    shutil.rmtree('reports', ignore_errors=True)

Path('reports/sca').mkdir(parents=True, exist_ok=True)
Path('reports/test_results').mkdir(parents=True, exist_ok=True)
Path('reports/coverage').mkdir(parents=True, exist_ok=True)

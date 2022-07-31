# Changelog2version

[![Downloads](https://pepy.tech/badge/changelog2version)](https://pepy.tech/project/changelog2version)
![Release](https://img.shields.io/github/v/release/brainelectronics/changelog2version?include_prereleases&color=success)
![Python](https://img.shields.io/badge/python3-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Update version info file with latest changelog version entry

---------------

## General

Create version info files based on the latest changelog entry.

## Installation

```bash
pip install changelog2version
```

## Usage

This example shows you how to parse the [repo's changelog](changelog.md) and
update the [package version file](src/changelog2version/version.py) with that
version.

```bash
changelog2version \
    --changelog_file changelog.md \
    --version_file src/changelog2version/version.py \
    --debug
```

## Credits

Based on the [PyPa sample project][ref-pypa-sample].

<!-- Links -->
[ref-pypa-sample]: https://github.com/pypa/sampleproject

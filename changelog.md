# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [x.y.z] - yyyy-mm-dd
### Added
### Changed
### Removed
### Fixed
-->
<!--
RegEx for release version from file
r"^\#\# \[\d{1,}[.]\d{1,}[.]\d{1,}\] \- \d{4}\-\d{2}-\d{2}$"
-->

## Released
## [0.1.1] - 2022-07-31
### Fixed
- Update root [`README`](README.md) file with usage instructions
- Use `0.0.0` as default in the checked in
  [package version file](src/changelog2version/version.py)
- Use `release/v1.5` branch of `pypa/gh-action-pypi-publish` in the
  [GitHub CI release workflow](.github/workflows/release.yml) file

## [0.1.0] - 2022-07-31
### Added
- This changelog file
- [`.coveragerc`](.coveragerc) file
- [`.flake8`](.flake8) file
- Script to [create report directories](create_report_dirs.py)
- [`unittest.cfg`](tests/unittest.cfg) file
- [`requirements.txt`](requirements.txt) file to setup required packages
- Initial [`changelog2version`](changelog2version) package

### Changed
- [`.gitignore`](.gitignore) file after fork to latest
  [Python gitignore template][ref-python-gitignore-template]
- [`setup.py`](setup.py) file after fork
- [`tox.ini`](tox.ini) file after fork to use `nose2` and create coverage
  report
- [GitHub CI release workflow](.github/workflows/release.yml) updated to run
  on `main` branch and update version file before package build
- [GitHub CI test workflow](.github/workflows/test.yml) updated to create
  package with updated version file, archive build artifacts, not running on
  `main` or `develop` branch and using package extras

### Removed
- Sample package in [`src`](src) after fork
- Sample package test in [`tests`](tests) after fork
- Data folder after fork

<!-- Links -->
[Unreleased]: https://github.com/brainelectronics/changelog2version/compare/0.1.1...develop

[0.1.1]: https://github.com/brainelectronics/changelog2version/tree/0.1.1
[0.1.0]: https://github.com/brainelectronics/changelog2version/tree/0.1.0

<!--
[ref-issue-1]: https://github.com/brainelectronics/changelog2version/issues/1
-->
[ref-python-gitignore-template]: https://github.com/github/gitignore/blob/e5323759e387ba347a9d50f8b0ddd16502eb71d4/Python.gitignore

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
## [0.4.0] - 2022-08-07
### Added
- Property `semver_data` to access extracted VersionInfo from parsed semver
  line in [`ExtractVersion class`](src/changelog2version/extract_version.py)
- Header and python version template file
- [`RenderVersionFile class`](src/changelog2version/render_version_file.py) to
  render template files with provided content, resolve [#5][ref-issue-5]
- [Examples folder](examples) with example C script to demonstrate template
  rendering on other files than python
- `--template_file` argument to specify a custom template file for rendering
- `--additional_template_data` to add custom data for the template rendering
- `c` is now a valid and supported file type of `--version_file_type`
- Documentation extended for new CLI args with more detailed examples
- `Jinja2` is a required package for this package

### Changed
- `parser_valid_file` function returns a resolved path
- `--version_file_type` is no longer case sensitive
- `--version_file` does no longer have to exist
- Run [GitHub CI unittest workflow](.github/workflows/unittest.yml) also on
  pull requests

### Removed
- Functions to update python version files from `update_version.py` script

### Fixed
- Only one job in [GitHub CI unittest workflow](.github/workflows/unittest.yml)
- Let [GitHub CI unittest workflow](.github/workflows/unittest.yml) fail when
  Codecov runs into errors during upload

## [0.3.0] - 2022-08-05
### Changed
- Regex to extract the first version line from a changelog supports the full
  feature scope of semantic versioning, resolve [#8][ref-issue-8]
- Regex to get the semantic versioning content of a version line supports the
  full feature scope of semantic versioning, resolve [#8][ref-issue-8]
- Testing of this package with `nose2` and coverage report generation with
  `coverage` including upload to [Codecov][ref-codecov-changelog2version] was
  moved to new [GitHub CI unittest workflow](.github/workflows/unittest.yml),
  resolve [#11][ref-issue-11]

### Removed
- `nose2` and `coverage` steps as well as upload to
  [Codecov][ref-codecov-changelog2version] removed from
  [GitHub CI release workflow](.github/workflows/release.yml) and
  [GitHub CI test workflow](.github/workflows/test.yml)

## [0.2.0] - 2022-08-03
### Added
- [`ExtractVersion class`](src/changelog2version/extract_version.py) to
  extract the version line from a changelog file and to parse the semver
  content from a version line, resolve [#4][ref-issue-4]
- `semver_line_regex` and `version_line_regex` args for `changelog2version` to
  provide custom regular expressions to parse a version line from a changelog
  and to extract the semver content from a line

### Changed
- Main parsing code of
  [`update_version script`](src/changelog2version/update_version.py) moved to
  new [`ExtractVersion class`](src/changelog2version/extract_version.py)
- Extend usage example in [`README`](README.md) file
- Rename [test data changelog files](tests/data/valid)
- Split unittest for `ExtractVersion` from `update_version` test
- Let the pipeline fail is there are flake8 violations

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
[Unreleased]: https://github.com/brainelectronics/changelog2version/compare/0.4.0...develop

[0.4.0]: https://github.com/brainelectronics/changelog2version/tree/0.4.0
[0.3.0]: https://github.com/brainelectronics/changelog2version/tree/0.3.0
[0.2.0]: https://github.com/brainelectronics/changelog2version/tree/0.2.0
[0.1.1]: https://github.com/brainelectronics/changelog2version/tree/0.1.1
[0.1.0]: https://github.com/brainelectronics/changelog2version/tree/0.1.0

[ref-issue-5]: https://github.com/brainelectronics/changelog2version/issues/5
[ref-issue-8]: https://github.com/brainelectronics/changelog2version/issues/8
[ref-issue-11]: https://github.com/brainelectronics/changelog2version/issues/11
[ref-issue-4]: https://github.com/brainelectronics/changelog2version/issues/4

[ref-codecov-changelog2version]: https://app.codecov.io/github/brainelectronics/changelog2version
[ref-python-gitignore-template]: https://github.com/github/gitignore/blob/e5323759e387ba347a9d50f8b0ddd16502eb71d4/Python.gitignore

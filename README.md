# Changelog2version

[![Downloads](https://pepy.tech/badge/changelog2version)](https://pepy.tech/project/changelog2version)
![Release](https://img.shields.io/github/v/release/brainelectronics/changelog2version?include_prereleases&color=success)
![Python](https://img.shields.io/badge/python3-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/github/brainelectronics/changelog2version/branch/main/graph/badge.svg)](https://app.codecov.io/github/brainelectronics/changelog2version)

Update version info file with latest changelog version entry

---------------

## General

Create version info files based on the latest changelog entry.

<!-- MarkdownTOC -->

- [Installation](#installation)
- [Usage](#usage)
    - [Available default template files](#available-default-template-files)
        - [C header file](#c-header-file)
        - [Python package file](#python-package-file)
- [Advanced](#advanced)
    - [Custom regular expressions](#custom-regular-expressions)
    - [Custom template file](#custom-template-file)
- [Credits](#credits)

<!-- /MarkdownTOC -->


## Installation

```bash
pip install changelog2version
```

## Usage

This example shows you how to parse the [repo's changelog](changelog.md) and
update the [package version file][ref-package-version-file] with that
version.

```bash
changelog2version \
    --changelog_file changelog.md \
    --version_file examples/version.py \
    --debug
```

### Available default template files

By default a Python version file is generated. Check the table below and the
example usage for further details and supported template files

| Type   | Parameter | Description |
| ------ | --------- | ----------- |
| Python | `py`      | See [example package version][ref-package-version-file] |
| C/CPP  | `c`       | Header file with available version info |

#### C header file

```bash
changelog2version \
    --changelog_file changelog.md \
    --version_file examples/version_info.h \
    --version_file_type c \
    --debug
```

```
//
//  version_info.h
//
//  Created automatically by script
//

#ifndef version_info_h
#define version_info_h

#define MAJOR_VERSION   0     //< major software version
#define MINOR_VERSION   4     //< minor software version
#define PATCH_VERSION   0     //< patch software version

#endif
```

#### Python package file

```bash
changelog2version \
    --changelog_file changelog.md \
    --version_file examples/version.py \
    --version_file_type py \
    --debug
```

```
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__version_info__ = ("0", "4", "0")
__version__ = '.'.join(__version_info__)

```

## Advanced

### Custom regular expressions

To extract a version line from a given changelog file with an alternative
regex, the `version_line_regex` argument can be used as shown below. The
expression is validated during the CLI argument parsing

```bash
changelog2version \
    --changelog_file changelog.md \
    --version_file src/changelog2version/version.py \
    --version_line_regex "^\#\# \[\d{1,}[.]\d{1,}[.]\d{1,}\]" \
    --debug
```

Same applies for a custom semver line regex in order to extract the semantic
version part from a full version line, use the `semver_line_regex` argument to
adjust the regular expression to your needs.

### Custom template file

Beside the default supported [template files][ref-templates-folder] users can
also provide custom template files.

This is the list of currently available variables

| Name                          | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| `major_version`               | Major version, incompatible API changes                   |
| `minor_version`               | Minor version, add functionality (backwards-compatible)   |
| `patch_version`               | Patch version, bug fixes (backwards-compatible)           |
| `prerelease_data`             | pre-release data, if available                            |
| `build_data`                  | Build metadata, if available                              |
| `file_name`                   | User specified name of rendered file                      |
| `file_name_without_suffix`    | User specified name of rendered file without suffix       |
| `template_name`               | Name of rendered template file                            |
| `template_name_without_suffix`| Name of rendered template file without suffix             |
| Custom keyword                | Provided by the user via `--additional_template_data`     |

```bash
additional_data="{\"creation_datetime\": \"$(date +"%Y-%m-%dT%H:%M:%S")\", \"machine_name\": \"$(whoami)\"}"
changelog2version \
    --changelog_file changelog.md \
    --version_file examples/version_info.c \
    --template_file examples/version_info.c.template \
    --additional_template_data "${additional_data}" \
    --debug

# or less fancy
changelog2version \
    --changelog_file changelog.md \
    --version_file examples/version_info.c \
    --template_file examples/version_info.c.template \
    --additional_template_data '{"creation_datetime": "2022-08-05T21:11:12", "machine_name": "Death Star"}' \
    --debug
```

Executing the created example file `examples/version_info.c` will print the
following content (datetime and creator might be different)

```
Script version is (major.minor.patch): 0.4.0
Prerelease data: None
Prerelease data: None
Creation datetime: 2022-08-05T21:11:12
Created by Death Star
```

## Credits

Based on the [PyPa sample project][ref-pypa-sample]. Also a big thank you to
the creators and maintainers of [SemVer.org][ref-semver] for their
documentation and [regex example][ref-semver-regex-example]

<!-- Links -->
[ref-package-version-file]: src/changelog2version/version.py
[ref-templates-folder]: src/changelog2version/templates
[ref-pypa-sample]: https://github.com/pypa/sampleproject
[ref-semver]: https://semver.org/
[ref-semver-regex-example]: https://regex101.com/r/Ly7O1x/3/

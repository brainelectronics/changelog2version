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
        - [JSON output](#json-output)
            - [Console](#console)
            - [File](#file)
- [Advanced](#advanced)
    - [Custom regular expressions](#custom-regular-expressions)
    - [Custom template file](#custom-template-file)
    - [Additional version info content](#additional-version-info-content)
- [Contributing](#contributing)
    - [Unittests](#unittests)
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

#### JSON output

The additional, optional argument `--pretty` will output the JSON data with an
indentation of 4 in order to provide the data in an easy to read format.

##### Console

```bash
changelog2version \
    --changelog_file changelog.md \
    --print \
    --debug
```

```json
{"info": {"version": "0.7.0", "description": "### Added\n- Changelog parsed as JSON contains a new key `description` like the PyPi package JSON info, compare to `https://pypi.org/pypi/changelog2version/json`, with the description/content of the latest change, see #19, relates to #18\n- Increase unittest coverage above 95%\n\n### Changed\n- Line breaks are no longer used in this changelog for enumerations\n- Issues are referenced as `#123` instead of `[#123][ref-issue-123]` to avoid explicit references at the bottom or some other location in the file\n- Output of `changelog2version` call with `--print` but without `--debug` option is JSON compatible\n"}, "releases": {"0.7.0": [{"upload_time": "2022-11-11"}], "0.6.0": [{"upload_time": "2022-10-26"}], "0.5.0": [{"upload_time": "2022-10-20"}], "0.4.0": [{"upload_time": "2022-08-07"}], "0.3.0": [{"upload_time": "2022-08-05"}], "0.2.0": [{"upload_time": "2022-08-03"}], "0.1.1": [{"upload_time": "2022-07-31"}], "0.1.0": [{"upload_time": "2022-07-31"}]}}
```

To get the latest version and description in the console as environment
variables use the following call

```bash
LATEST_VERSION=$(changelog2version --changelog_file changelog.md --print | python -c "import sys, json; print(json.load(sys.stdin)['info']['version'])")
LATEST_CHANGE=$(changelog2version --changelog_file changelog.md --print | python -c "import sys, json; print(json.load(sys.stdin)['info']['description'])")

echo "The latest version extracted from the changelog is ${LATEST_VERSION}"
# The latest version extracted from the changelog is 0.7.0

echo "Description of the latest change"
echo "${LATEST_CHANGE}"
# ### Added
# - Changelog parsed as JSON contains a new key `description` like the PyPi package JSON info, compare to `https://pyp
# i.org/pypi/changelog2version/json`, with the description/content of the latest change, see #19, relates to #18
# - Increase unittest coverage above 95%

# ### Changed
# - Line breaks are no longer used in this changelog for enumerations
# - Issues are referenced as `#123` instead of `[#123][ref-issue-123]` to avoid explicit references at the bottom or s
# ome other location in the file
# - Output of `changelog2version` call with `--print` but without `--debug` option is JSON compatible
```

##### File

```bash
changelog2version \
    --changelog_file changelog.md \
    --output changelog.json \
    --pretty \
    --debug
```

See [example JSON file][ref-example-json-file]

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

### Additional version info content

To create custom release candidate packages the python version file variable
`__version__` can be exended with a custom string.

Choose the additional version info content carefully as not everything is
supported by PyPi, see the
[Python Core metadata specifications][ref-py-core-metadata-spec] and
[PEP440][ref-pep440]

```bash
changelog2version \
    --changelog_file changelog.md \
    --version_file examples/version.py \
    --version_file_type py \
    --additional_version_info="rc1234" \
    --debug
```

```
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__version_info__ = ("0", "5", "0")
__version__ = '.'.join(__version_info__) + '-rc1234'

```

## Contributing

### Unittests

Run the unittests locally with the following command after installing this
package in a virtual environment or by using `tox` to create one on each run.

```bash
# install the package with all its development dependencies
pip install .[dev]

# run all tests
nose2 --config tests/unittest.cfg

# run only one specific tests
nose2 tests.test_extract_version.TestExtractVersion.test_version_line_regex
```

Generate the coverage files with

```bash
python create_report_dirs.py
coverage html
```

The coverage report is placed at `reports/coverage/html/index.html`

## Credits

Based on the [PyPa sample project][ref-pypa-sample]. Also a big thank you to
the creators and maintainers of [SemVer.org][ref-semver] for their
documentation and [regex example][ref-semver-regex-example]

<!-- Links -->
[ref-package-version-file]: src/changelog2version/version.py
[ref-templates-folder]: src/changelog2version/templates
[ref-example-json-file]: examples/changelog.json
[ref-py-core-metadata-spec]: https://packaging.python.org/specifications/core-metadat
[ref-pep440]: https://peps.python.org/pep-0440/
[ref-pypa-sample]: https://github.com/pypa/sampleproject
[ref-semver]: https://semver.org/
[ref-semver-regex-example]: https://regex101.com/r/Ly7O1x/3/

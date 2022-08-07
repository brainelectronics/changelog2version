#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Update version info in template file with latest changelog version

The changelog and package version shall always be aligned. This script can be
used to render a python version file from the latest changelog entry.
This changelog entry shall follow the semantic version pattern, see
https://semver.org/ and shall match the following pattern:

## [x.y.z] - yyyy-mm-dd

The line shall start with two hashtags followed by a single space. The semver
with x, y and z as non-negative integers, seperated by a dot and surrounded by
square brackets. Followed by a space, a dash, another space and the ISO8601
formatted date. Additional timestamps after the data, seperated from the date
by a single space or a capital "T", are optional.
The semantic version tag inside the square brackets supports the full scope.
"""

import argparse
import fileinput
import json
import logging
from pathlib import Path
import re
import semver
from sys import stdout

from .extract_version import ExtractVersion
from .render_version_file import RenderVersionFile


def parser_valid_file(parser: argparse.ArgumentParser, arg: str) -> Path:
    """
    Determine whether file exists.
    :param      parser:                 The parser
    :type       parser:                 parser object
    :param      arg:                    The file to check
    :type       arg:                    str
    :raise      argparse.ArgumentError: Argument is not a file
    :returns:   Input file path, parser error is thrown otherwise.
    :rtype:     Path
    """
    if not Path(arg).is_file():
        parser.error("The file {} does not exist!".format(arg))
    else:
        return Path(arg).resolve()


def validate_regex(parser: argparse.ArgumentParser, arg: str) -> str:
    """
    Validate given regex pattern
    :param      parser:                 The parser
    :type       parser:                 parser object
    :param      arg:                    The regex pattern to check
    :type       arg:                    str
    :raise      argparse.ArgumentError: Argument is not a file
    :returns:   Regex pattern, parser error is thrown otherwise.
    :rtype:     str
    """
    try:
        re.compile(arg)
    except re.error:
        parser.error("The regex pattern '{}' is invalid".format(arg))
    return arg


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments.
    :raise      argparse.ArgumentError  Argparse error
    :return:    argparse object
    """
    parser = argparse.ArgumentParser(description="""
    Update version info file based on changelog entry
    """, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # default arguments
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Output logger messages to stderr')

    # specific arguments
    parser.add_argument('--changelog_file',
                        dest='changelog_file',
                        required=True,
                        type=lambda x: parser_valid_file(parser, x),
                        help='Path to changelog file')

    parser.add_argument('--version_file',
                        dest='version_file',
                        required=True,
                        help='Path to rendered file')

    parser.add_argument('--version_file_type',
                        dest='version_file_type',
                        required=False,
                        choices=['py', 'c'],
                        default='py',
                        type=lambda x: x.lower(),
                        help='Type of version file to generate')

    parser.add_argument('--template_file',
                        dest='template_file',
                        required=False,
                        type=lambda x: parser_valid_file(parser, x),
                        help='Path to template version file')

    parser.add_argument('--additional_template_data',
                        dest='additional_template_data',
                        required=False,
                        type=json.loads,
                        help='Additional data as JSON to render the template')

    parser.add_argument('--version_line_regex',
                        dest='version_line_regex',
                        required=False,
                        type=lambda x: validate_regex(parser, x),
                        help='Regex to extract complete version line from a '
                             'changelog')

    parser.add_argument('--semver_line_regex',
                        dest='semver_line_regex',
                        required=False,
                        type=lambda x: validate_regex(parser, x),
                        help='Regex to extract semver part of from a version '
                             'line')

    parsed_args = parser.parse_args()

    return parsed_args


def main():
    # parse CLI arguments
    args = parse_arguments()

    custom_format = '[%(asctime)s] [%(levelname)-8s] [%(filename)-15s @'\
                    ' %(funcName)-15s:%(lineno)4s] %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=custom_format,
                        stream=stdout)
    logger = logging.getLogger(__name__)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    # changelog_file = Path(args.changelog_file).resolve()
    changelog_file = args.changelog_file
    version_file = Path(args.version_file).resolve()
    template_file = args.template_file
    version_file_type = args.version_file_type
    additional_template_data = args.additional_template_data
    version_line_regex = args.version_line_regex
    semver_line_regex = args.semver_line_regex

    logger.debug("Using changelog file '{}' to update version file '{}'".
                 format(changelog_file, version_file))

    version_extractor = ExtractVersion(logger=logger)

    if semver_line_regex:
        logger.debug("Use this regex to get the semver part from the "
                     "version line: {}".format(semver_line_regex))
        version_extractor.semver_line_regex = semver_line_regex

    if version_line_regex:
        logger.debug("Use this regex to get the version line from the "
                     "changelog file: {}".format(version_line_regex))
        version_extractor.version_line_regex = version_line_regex

    version_line = version_extractor.parse_changelog(changelog_file)
    semver_string = version_extractor.parse_semver_line(version_line)

    file_renderer = RenderVersionFile()
    semver_data = version_extractor.semver_data
    version_file_content = {
        "major_version": semver_data.major,
        "minor_version": semver_data.minor,
        "patch_version": semver_data.patch,
        "prerelease_data": semver_data.prerelease,
        "build_data": semver_data.build
    }
    if additional_template_data:
        version_file_content.update(additional_template_data)

    if not template_file:
        # no template file specified, use package template file
        template_file_map = {
            "py": "version.py.template",
            "c": "version.h.template",
        }

        if version_file_type in template_file_map:
            template_file = template_file_map[version_file_type]
            logger.info("Selected '{}' based on version_file_type: '{}'".
                        format(template_file, version_file_type))
        else:
            raise KeyError("Either specify a custom template file or choose"
                           "a template from this list: {}".
                           format(template_file_map.keys()))

    rendered_content = file_renderer.render_file(
        template=template_file,
        file_path=version_file,
        content=version_file_content)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Extract a single version line from a changelog and extract the semver content
from this line
"""

import logging
from pathlib import Path
import re
from semver import VersionInfo
from sys import stdout
from typing import Optional


class ExtractVersionError(Exception):
    """Base class for exceptions in this module."""
    pass


class ExtractVersion(object):
    """Extract the version line and SemVer part from a changelog file"""
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Init ExtractVersion class

        :param      logger:             Logger object
        :type       logger:             Optional[logging.Logger]
        """
        if logger is None:
            logger = self._create_logger()
        self._logger = logger
        self._semver_data = VersionInfo(*(0, 0, 0))

        self._semver_line_regex = (
            r"^(?P<major>0|[1-9]\d*)\."     # major version part
            r"(?P<minor>0|[1-9]\d*)\."      # minor version part
            r"(?P<patch>0|[1-9]\d*)"        # bugfix/patch version part
            # optional prerelease version part, starting with a "-"
            r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"    # noqa
            # optional build metadata version part, starting with a "+"
            r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
        )

        self._version_line_regex = (
            # begin of line with two "#" followed by a single space
            r"(?P<title_begin>\#\#)[ ]{1}"
            # anything after a "["
            r"\[(?P<potential_semver>("
            # three numbers with one or more digits, seperated by dot
            r"(\d{1,}\.\d{1,}\.\d{1,})"
            r"([-+]?)"  # zero or one of either a "-" or "+" character
            # r"(.*)"  # any character zero or more times
            r"([a-zA-Z.+-d]*)"  # any character (a-Z), dot, "-", "+" or number
                                # for zero or more times
            r")(?=\]))\]"    # positive lookahead for the "]" and the "]"
            r"[ ]{1}\-[ ]{1}"     # exactly one space, "-", exactly one space
            r"(?P<datetime>\d{4}\-\d{2}-\d{2})"     # datetime as YYYY-MM-DD
            r"(([T ]{1})"   # seperation between date and time by "T" or space
            r"(?P<timestamp>\d{2,}:\d{2,}:\d{2,}?))?"   # time as HH:MM:SS
        )

    @property
    def version_line_regex(self) -> str:
        """
        Get regex to extract complete version line from changelog

        :returns:   Regex of the complete version line
        :rtype:     str
        """
        return self._version_line_regex

    @version_line_regex.setter
    def version_line_regex(self, value: str) -> None:
        """
        Set regex to extract complete version line from changelog

        :param      value:  Regex to get the complete version line
        :type       value:  str
        """
        try:
            re.compile(value)
            self._version_line_regex = value
        except re.error:
            raise ExtractVersionError("Invalid regex pattern")

    @property
    def semver_line_regex(self) -> str:
        """
        Get regex to extract the semver part from the complete version line

        :returns:   Regex of the semver part
        :rtype:     str
        """
        return self._semver_line_regex

    @semver_line_regex.setter
    def semver_line_regex(self, value: str) -> None:
        """
        Set regex to extract the semver part from the complete version line

        :param      value:  Regex to get the semver part
        :type       value:  str
        """
        try:
            re.compile(value)
            self._semver_line_regex = value
        except re.error:
            raise ExtractVersionError("Invalid regex pattern")

    @property
    def semver_data(self) -> VersionInfo:
        """
        Get VersionInfo object with latest SemVer data

        :returns:   The version information
        :rtype:     VersionInfo
        """
        return self._semver_data

    @semver_data.setter
    def semver_data(self, value: VersionInfo) -> None:
        """
        Set SemVer data

        :param      value:  The value
        :type       value:  VersionInfo
        """
        if isinstance(value, VersionInfo):
            self._semver_data = value
        else:
            raise ExtractVersionError("Value is not of type VersionInfo")

    @staticmethod
    def _create_logger(logger_name: str = None) -> logging.Logger:
        """
        Create a logger

        :param      logger_name:  The logger name
        :type       logger_name:  str, optional

        :returns:   Configured logger
        :rtype:     logging.Logger
        """
        custom_format = '[%(asctime)s] [%(levelname)-8s] [%(filename)-15s @'\
                        ' %(funcName)-15s:%(lineno)4s] %(message)s'

        # configure logging
        logging.basicConfig(level=logging.INFO,
                            format=custom_format,
                            stream=stdout)

        if logger_name and (isinstance(logger_name, str)):
            logger = logging.getLogger(logger_name)
        else:
            logger = logging.getLogger(__name__)

        # set the logger level to DEBUG if specified differently
        logger.setLevel(logging.DEBUG)

        return logger

    def parse_changelog(self, changelog_file: Path) -> str:
        """
        Parse the changelog for the first matching version line

        :param      changelog_file:  The path to the changelog file
        :type       changelog_file:  Path

        :returns:   Extracted semantic version string
        :rtype:     str
        """
        release_version_line = ""

        with open(changelog_file, "r") as f:
            for line in f:
                match = re.search(self.version_line_regex, line)
                if match:
                    release_version_line = match.group()
                    break

        self._logger.debug("First matching release version line: '{}'".
                           format(release_version_line))

        return release_version_line

    def parse_semver_line(self, release_version_line: str) -> str:
        """
        Parse a version line for a semantic version

        Examples of a valid SemVer line:
        - "## [0.2.0] - 2022-05-19"
        - "## [107.3.18] - 1900-01-01 12:34:56"
        - "## [1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay] - 2012-01-02"    # noqa

        :param      release_version_line:  The release version line
        :type       release_version_line:  str

        :returns:   Semantic version string, e.g. "0.2.0"
        :rtype:     str
        """
        semver_string = "0.0.0"

        # try to extract any content between square brackets
        match = re.search(r"\[(.*?)\]", release_version_line)
        if not match:
            return semver_string

        # the potential semver content is the first group of the complete line
        potential_semver = match.group(1)

        # try to extract semver from release version line
        match = re.search(self.semver_line_regex, potential_semver)

        if match:
            semver_string = match.group()
            if not VersionInfo.isvalid(semver_string):
                self._logger.error("Parsed SemVer string is invalid, check "
                                   "the changelog format")
                raise ValueError("Invalid SemVer string")
            self._logger.debug("Extracted SemVer string: '{}'".
                               format(semver_string))
            self.semver_data = VersionInfo.parse(semver_string)
        else:
            self._logger.warning("No SemVer string found in given release "
                                 "version line: '{}'".
                                 format(release_version_line))

        return semver_string

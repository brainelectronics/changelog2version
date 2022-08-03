#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Extract a single version line from a changelog and extract the semver content
from this line
"""

import logging
from pathlib import Path
import re
import semver
from sys import stdout
from typing import Optional


class ExtractVersionError(Exception):
    """Base class for exceptions in this module."""
    pass


class ExtractVersion(object):
    """Extract the version line and SemVer part from a changelog file"""
    def __init__(self,
                 # version_line_regex: Optional[str] = None,
                 # semver_line_regex: Optional[str] = None,
                 logger: Optional[logging.Logger] = None):
        """
        Init ExtractVersion class

        :param      version_line_regex: Regex for the complete version line
        :type       version_line_regex: Optional[str]
        :param      semver_line_regex:  Regex for the semver part of the
                                        complete version line
        :type       semver_line_regex:  Optional[str]
        :param      logger:             Logger object
        :type       logger:             Optional[logging.Logger]
        """
        if logger is None:
            logger = self._create_logger()
        self._logger = logger

        # append "$" to match only ISO8601 dates without additional timestamps
        self._version_line_regex = r"^\#\# \[\d{1,}[.]\d{1,}[.]\d{1,}\] \- \d{4}\-\d{2}-\d{2}"    # noqa
        self._semver_line_regex = r"\[\d{1,}[.]\d{1,}[.]\d{1,}\]"

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

    def _create_logger(self, logger_name: str = None) -> logging.Logger:
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

        :param      release_version_line:  The release version line
        :type       release_version_line:  str

        :returns:   Semantic version string, e.g. "0.2.0"
        :rtype:     str
        """
        semver_string = "0.0.0"

        # extract semver from release version line
        match = re.search(self.semver_line_regex, release_version_line)
        if match:
            semver_string = match.group()
            # remove '[' and ']' from semver_string
            semver_string = re.sub(r"[\[\]]", "", semver_string)
            if not semver.VersionInfo.isvalid(semver_string):
                self._logger.error("Parsed SemVer string is invalid, check "
                                   "the changelog format")
                raise ValueError("Invalid SemVer string")
            self._logger.debug("Extracted SemVer string: '{}'".
                               format(semver_string))
        else:
            self._logger.warning("No SemVer string found in given release "
                                 "version line: '{}'".
                                 format(release_version_line))

        return semver_string

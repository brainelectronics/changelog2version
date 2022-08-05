#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Unittest for testing the extract_version file"""

import logging
from nose2.tools import params
from pathlib import Path
from sys import stdout
import unittest
from unittest.mock import patch, mock_open

from changelog2version.extract_version import ExtractVersion, \
    ExtractVersionError


class TestExtractVersion(unittest.TestCase):

    def setUp(self) -> None:
        """Run before every test method"""
        # define a format
        custom_format = '[%(asctime)s] [%(levelname)-8s] [%(filename)-15s @'\
                        ' %(funcName)-15s:%(lineno)4s] %(message)s'

        # set basic config and level for all loggers
        logging.basicConfig(level=logging.INFO,
                            format=custom_format,
                            stream=stdout)

        # create a logger for this TestSuite
        self.test_logger = logging.getLogger(__name__)
        self.package_logger = logging.getLogger('UpdateVersion')

        # set the test logger level
        self.test_logger.setLevel(logging.DEBUG)
        self.package_logger.setLevel(logging.DEBUG)

        self._here = Path(__file__).parent

        self.ev = ExtractVersion()

    def tearDown(self) -> None:
        """Run after every test method"""
        pass

    def test_version_line_regex(self) -> None:
        """Test property version_line_regex"""
        self.ev.version_line_regex = "gray|grey"

        with self.assertRaises(ExtractVersionError) as context:
            self.ev.version_line_regex = "["

        self.assertEqual("Invalid regex pattern", str(context.exception))

    def test_semver_line_regex(self) -> None:
        """Test property semver_regex"""
        self.ev.semver_line_regex = "gray|grey"

        with self.assertRaises(ExtractVersionError) as context:
            self.ev.semver_line_regex = "["

        self.assertEqual("Invalid regex pattern", str(context.exception))

    @unittest.skip("Not yet implemented")
    def test__create_logger(self):
        """Test logger creation"""
        pass

    @params(
        ("changelog_with_date.md", "## [1.2.3] - 2022-07-31"),
        ("changelog_with_date_and_time.md",
         "## [93.10.1] - 2022-07-31 12:34:56"),
    )
    def test_parse_changelog_file(self,
                                  file_name: str,
                                  expectation: str) -> None:
        """Test parse_changelog"""
        changelog = self._here / 'data' / 'valid' / file_name

        result = self.ev.parse_changelog(changelog_file=changelog)
        self.test_logger.debug('Extracted "{}" from "{}"'.
                               format(result, changelog.name))

        self.assertIsInstance(result, str)
        self.assertEqual(expectation, result)

    @params(
        # valid semver release version lines
        ("## [1.2.3] - 2012-01-02", "## [1.2.3] - 2012-01-02"),
        (
            "## [1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay] - "
            "2012-01-02",
            "## [1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay] - "
            "2012-01-02",
        ),
        (
            "## [1.2.3] - 2012-01-02 12:34:56",
            "## [1.2.3] - 2012-01-02 12:34:56"
        ),
        (
            "## [1.2.3] - 2012-01-02T12:34:56",
            "## [1.2.3] - 2012-01-02T12:34:56"
        ),

        # invalid version lines
        (
            # missing "## " at the beginning
            "[1.2.0] - 1900-01-01", ""
        ),
        (
            # year does not follow YYYY format
            "## [1.2.3] - 19-01-01", ""
        ),
        (
            # month does not follow MM format
            "## [1.3.0] - 1900-1-01", ""
        ),
        (
            # day does not follow DD format
            "## [1.4.7] - 1900-01-1", ""
        ),
        (
            # month and day does not follow MM-DD form
            "## [1.5.8] - 1900-1-1", ""
        ),
        (
            # year, month and day does not follow YYYY-MM-DD format
            "## [1.6.0] - 19-1-1", ""
        ),
        (
            # invalid character "!" between square brackets
            "## [1.2.3!] - 2012-01-02", ""
        ),
        # (
        #     # invalid timestamp separation character
        #     "## [1.2.3] - 2012-01-02-12:34:56", ""
        # ),
        # there will be a problem on the first of January 10.000 :)
    )
    def test_parse_changelog_line(self, line: str, expectation: str) -> None:
        """
        Test parse changelog

        Use one line as mocked file content

        :param      line:           The mocked file data
        :type       line:           str
        :param      expectation:    Expected, parsed result
        :type       expectation:    str
        """
        changelog_file = '/dev/null'
        with patch('builtins.open', mock_open(read_data=line)):
            result = self.ev.parse_changelog(changelog_file=changelog_file)
            self.test_logger.debug('Extracted "{}" from "{}"'.
                                   format(result, changelog_file))

            self.assertIsInstance(result, str)
            self.assertEqual(expectation, result)

    @params(
        # test strings taken from https://regex101.com/r/Ly7O1x/3/ and adopted
        # valid semver release version lines without timestamp
        ("## [1.2.3] - 2012-01-02", "1.2.3"),
        ("## [10.20.30] - 2012-01-02", "10.20.30"),
        ("## [1.1.2-prerelease+meta] - 2012-01-02", "1.1.2-prerelease+meta"),
        ("## [1.1.2+meta] - 2012-01-02", "1.1.2+meta"),
        ("## [1.1.2+meta-valid] - 2012-01-02", "1.1.2+meta-valid"),
        ("## [1.0.0-alpha] - 2012-01-02", "1.0.0-alpha"),
        ("## [1.0.0-beta] - 2012-01-02", "1.0.0-beta"),
        ("## [1.0.0-alpha.beta] - 2012-01-02", "1.0.0-alpha.beta"),
        ("## [1.0.0-alpha.beta.1] - 2012-01-02", "1.0.0-alpha.beta.1"),
        ("## [1.0.0-alpha.1] - 2012-01-02", "1.0.0-alpha.1"),
        ("## [1.0.0-alpha0.valid] - 2012-01-02", "1.0.0-alpha0.valid"),
        ("## [1.0.0-alpha.0valid] - 2012-01-02", "1.0.0-alpha.0valid"),
        (
            "## [1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay] - "
            "2012-01-02",
            "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay"
        ),
        ("## [1.0.0-rc.1+build.1] - 2012-01-02", "1.0.0-rc.1+build.1"),
        ("## [2.0.0-rc.1+build.123] - 2012-01-02", "2.0.0-rc.1+build.123"),
        ("## [1.2.3-beta] - 2012-01-02", "1.2.3-beta"),
        ("## [10.2.3-DEV-SNAPSHOT] - 2012-01-02", "10.2.3-DEV-SNAPSHOT"),
        ("## [1.2.3-SNAPSHOT-123] - 2012-01-02", "1.2.3-SNAPSHOT-123"),
        ("## [1.0.0] - 2012-01-02", "1.0.0"),
        ("## [2.0.0] - 2012-01-02", "2.0.0"),
        ("## [1.1.7] - 2012-01-02", "1.1.7"),
        ("## [2.0.0+build.1848] - 2012-01-02", "2.0.0+build.1848"),
        ("## [2.0.1-alpha.1227] - 2012-01-02", "2.0.1-alpha.1227"),
        ("## [1.0.0-alpha+beta] - 2012-01-02", "1.0.0-alpha+beta"),
        (
            "## [1.2.3----RC-SNAPSHOT.12.9.1--.12+788] - 2012-01-02",
            "1.2.3----RC-SNAPSHOT.12.9.1--.12+788"
        ),
        (
            "## [1.2.3----R-S.12.9.1--.12+meta] - 2012-01-02",
            "1.2.3----R-S.12.9.1--.12+meta"
        ),
        (
            "## [1.2.3----RC-SNAPSHOT.12.9.1--.12] - 2012-01-02",
            "1.2.3----RC-SNAPSHOT.12.9.1--.12"
        ),
        (
            "## [1.0.0+0.build.1-rc.10000aaa-kk-0.1] - 2012-01-02",
            "1.0.0+0.build.1-rc.10000aaa-kk-0.1"
        ),
        (
            "## [99999999999999999999999.999999999999999999.99999999999999999]"
            " - 2012-01-02",
            "99999999999999999999999.999999999999999999.99999999999999999"
        ),
        ("## [1.0.0-0A.is.legal] - 2012-01-02", "1.0.0-0A.is.legal"),

        # valid release version lines with timestamp
        # timestamp shall be seperated from date by
        #   - "T" to follow the ISO8601 norm
        #   - a single space
        # timestamp seperated from date by a single "T"
        ("## [1.2.3] - 2012-01-02T12:34:56", "1.2.3"),
        ("## [10.20.30] - 2012-01-02T12:34:56", "10.20.30"),
        (
            "## [1.1.2-prerelease+meta] - 2012-01-02T12:34:56",
            "1.1.2-prerelease+meta"
        ),
        ("## [1.1.2+meta] - 2012-01-02T12:34:56", "1.1.2+meta"),
        ("## [1.1.2+meta-valid] - 2012-01-02T12:34:56", "1.1.2+meta-valid"),
        ("## [1.0.0-alpha] - 2012-01-02T12:34:56", "1.0.0-alpha"),
        ("## [1.0.0-beta] - 2012-01-02T12:34:56", "1.0.0-beta"),
        ("## [1.0.0-alpha.beta] - 2012-01-02T12:34:56", "1.0.0-alpha.beta"),
        (
            "## [1.0.0-alpha.beta.1] - 2012-01-02T12:34:56",
            "1.0.0-alpha.beta.1"
        ),
        ("## [1.0.0-alpha.1] - 2012-01-02T12:34:56", "1.0.0-alpha.1"),
        (
            "## [1.0.0-alpha0.valid] - 2012-01-02T12:34:56",
            "1.0.0-alpha0.valid"
        ),
        (
            "## [1.0.0-alpha.0valid] - 2012-01-02T12:34:56",
            "1.0.0-alpha.0valid"
        ),
        (
            "## [1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay] - "
            "2012-01-02T12:34:56",
            "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay"
        ),
        (
            "## [1.0.0-rc.1+build.1] - 2012-01-02T12:34:56",
            "1.0.0-rc.1+build.1"
        ),
        (
            "## [2.0.0-rc.1+build.123] - 2012-01-02T12:34:56",
            "2.0.0-rc.1+build.123"
        ),
        ("## [1.2.3-beta] - 2012-01-02T12:34:56", "1.2.3-beta"),
        (
            "## [10.2.3-DEV-SNAPSHOT] - 2012-01-02T12:34:56",
            "10.2.3-DEV-SNAPSHOT"
        ),
        (
            "## [1.2.3-SNAPSHOT-123] - 2012-01-02T12:34:56",
            "1.2.3-SNAPSHOT-123"
        ),
        ("## [1.0.0] - 2012-01-02T12:34:56", "1.0.0"),
        ("## [2.0.0] - 2012-01-02T12:34:56", "2.0.0"),
        ("## [1.1.7] - 2012-01-02T12:34:56", "1.1.7"),
        ("## [2.0.0+build.1848] - 2012-01-02T12:34:56", "2.0.0+build.1848"),
        ("## [2.0.1-alpha.1227] - 2012-01-02T12:34:56", "2.0.1-alpha.1227"),
        ("## [1.0.0-alpha+beta] - 2012-01-02T12:34:56", "1.0.0-alpha+beta"),
        (
            "## [1.2.3----RC-SNAPSHOT.12.9.1--.12+788] - 2012-01-02T12:34:56",
            "1.2.3----RC-SNAPSHOT.12.9.1--.12+788"
        ),
        (
            "## [1.2.3----R-S.12.9.1--.12+meta] - 2012-01-02T12:34:56",
            "1.2.3----R-S.12.9.1--.12+meta"
        ),
        (
            "## [1.2.3----RC-SNAPSHOT.12.9.1--.12] - 2012-01-02T12:34:56",
            "1.2.3----RC-SNAPSHOT.12.9.1--.12"
        ),
        (
            "## [1.0.0+0.build.1-rc.10000aaa-kk-0.1] - 2012-01-02T12:34:56",
            "1.0.0+0.build.1-rc.10000aaa-kk-0.1"
        ),
        (
            "## [99999999999999999999999.999999999999999999.99999999999999999]"
            " - 2012-01-02T12:34:56",
            "99999999999999999999999.999999999999999999.99999999999999999"),
        ("## [1.0.0-0A.is.legal] - 2012-01-02T12:34:56", "1.0.0-0A.is.legal"),

        # timestamp seperated from date by a single space
        ("## [1.2.3] - 2012-01-02 12:34:56", "1.2.3"),
        ("## [10.20.30] - 2012-01-02 12:34:56", "10.20.30"),
        (
            "## [1.1.2-prerelease+meta] - 2012-01-02 12:34:56",
            "1.1.2-prerelease+meta"
        ),
        ("## [1.1.2+meta] - 2012-01-02 12:34:56", "1.1.2+meta"),
        ("## [1.1.2+meta-valid] - 2012-01-02 12:34:56", "1.1.2+meta-valid"),
        ("## [1.0.0-alpha] - 2012-01-02 12:34:56", "1.0.0-alpha"),
        ("## [1.0.0-beta] - 2012-01-02 12:34:56", "1.0.0-beta"),
        ("## [1.0.0-alpha.beta] - 2012-01-02 12:34:56", "1.0.0-alpha.beta"),
        (
            "## [1.0.0-alpha.beta.1] - 2012-01-02 12:34:56",
            "1.0.0-alpha.beta.1"
        ),
        ("## [1.0.0-alpha.1] - 2012-01-02 12:34:56", "1.0.0-alpha.1"),
        (
            "## [1.0.0-alpha0.valid] - 2012-01-02 12:34:56",
            "1.0.0-alpha0.valid"
        ),
        (
            "## [1.0.0-alpha.0valid] - 2012-01-02 12:34:56",
            "1.0.0-alpha.0valid"
        ),
        (
            "## [1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay] - "
            "2012-01-02 12:34:56",
            "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay"
        ),
        (
            "## [1.0.0-rc.1+build.1] - 2012-01-02 12:34:56",
            "1.0.0-rc.1+build.1"
        ),
        (
            "## [2.0.0-rc.1+build.123] - 2012-01-02 12:34:56",
            "2.0.0-rc.1+build.123"
        ),
        ("## [1.2.3-beta] - 2012-01-02 12:34:56", "1.2.3-beta"),
        (
            "## [10.2.3-DEV-SNAPSHOT] - 2012-01-02 12:34:56",
            "10.2.3-DEV-SNAPSHOT"
        ),
        (
            "## [1.2.3-SNAPSHOT-123] - 2012-01-02 12:34:56",
            "1.2.3-SNAPSHOT-123"
        ),
        ("## [1.0.0] - 2012-01-02 12:34:56", "1.0.0"),
        ("## [2.0.0] - 2012-01-02 12:34:56", "2.0.0"),
        ("## [1.1.7] - 2012-01-02 12:34:56", "1.1.7"),
        ("## [2.0.0+build.1848] - 2012-01-02 12:34:56", "2.0.0+build.1848"),
        ("## [2.0.1-alpha.1227] - 2012-01-02 12:34:56", "2.0.1-alpha.1227"),
        ("## [1.0.0-alpha+beta] - 2012-01-02 12:34:56", "1.0.0-alpha+beta"),
        (
            "## [1.2.3----RC-SNAPSHOT.12.9.1--.12+788] - 2012-01-02 12:34:56",
            "1.2.3----RC-SNAPSHOT.12.9.1--.12+788"
        ),
        (
            "## [1.2.3----R-S.12.9.1--.12+meta] - 2012-01-02 12:34:56",
            "1.2.3----R-S.12.9.1--.12+meta"
        ),
        (
            "## [1.2.3----RC-SNAPSHOT.12.9.1--.12] - 2012-01-02 12:34:56",
            "1.2.3----RC-SNAPSHOT.12.9.1--.12"
        ),
        (
            "## [1.0.0+0.build.1-rc.10000aaa-kk-0.1] - 2012-01-02 12:34:56",
            "1.0.0+0.build.1-rc.10000aaa-kk-0.1"
        ),
        (
            "## [99999999999999999999999.999999999999999999.99999999999999999]"
            " - 2012-01-02 12:34:56",
            "99999999999999999999999.999999999999999999.99999999999999999"
        ),
        ("## [1.0.0-0A.is.legal] - 2012-01-02 12:34:56", "1.0.0-0A.is.legal"),

        # invalid release version lines
        ("## [1] - 1970-01-01", "0.0.0"),
        ("## [1.2] - 1970-01-01", "0.0.0"),
        ("## [1.2.3-0123] - 1970-01-01", "0.0.0"),
        ("## [1.2.3-0123.0123] - 1970-01-01", "0.0.0"),
        ("## [1.1.2+.123] - 1970-01-01", "0.0.0"),
        ("## [+invalid] - 1970-01-01", "0.0.0"),
        ("## [-invalid] - 1970-01-01", "0.0.0"),
        ("## [-invalid+invalid] - 1970-01-01", "0.0.0"),
        ("## [-invalid.01] - 1970-01-01", "0.0.0"),
        ("## [alpha] - 1970-01-01", "0.0.0"),
        ("## [alpha.beta] - 1970-01-01", "0.0.0"),
        ("## [alpha.beta.1] - 1970-01-01", "0.0.0"),
        ("## [alpha.1] - 1970-01-01", "0.0.0"),
        ("## [alpha+beta] - 1970-01-01", "0.0.0"),
        ("## [alpha_beta] - 1970-01-01", "0.0.0"),
        ("## [alpha.] - 1970-01-01", "0.0.0"),
        ("## [alpha..] - 1970-01-01", "0.0.0"),
        ("## [beta] - 1970-01-01", "0.0.0"),
        ("## [1.0.0-alpha_beta] - 1970-01-01", "0.0.0"),
        ("## [-alpha.] - 1970-01-01", "0.0.0"),
        ("## [1.0.0-alpha..] - 1970-01-01", "0.0.0"),
        ("## [1.0.0-alpha..1] - 1970-01-01", "0.0.0"),
        ("## [1.0.0-alpha...1] - 1970-01-01", "0.0.0"),
        ("## [1.0.0-alpha....1] - 1970-01-01", "0.0.0"),
        ("## [1.0.0-alpha.....1] - 1970-01-01", "0.0.0"),
        ("## [1.0.0-alpha......1] - 1970-01-01", "0.0.0"),
        ("## [1.0.0-alpha.......1] - 1970-01-01", "0.0.0"),
        ("## [01.1.1] - 1970-01-01", "0.0.0"),
        ("## [1.01.1] - 1970-01-01", "0.0.0"),
        ("## [1.1.01] - 1970-01-01", "0.0.0"),
        ("## [1.2] - 1970-01-01", "0.0.0"),
        ("## [1.2.3.DEV] - 1970-01-01", "0.0.0"),
        ("## [1.2-SNAPSHOT] - 1970-01-01", "0.0.0"),
        (
            "## [1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788] - 1970-01-01",
            "0.0.0"
        ),
        ("## [1.2-RC-SNAPSHOT] - 1970-01-01", "0.0.0"),
        ("## [-1.0.3-gamma+b7718] - 1970-01-01", "0.0.0"),
        ("## [+justmeta] - 1970-01-01", "0.0.0"),
        ("## [9.8.7+meta+meta] - 1970-01-01", "0.0.0"),
        ("## [9.8.7-whatever+meta+meta] - 1970-01-01", "0.0.0"),
        (
            "## [99999999999999999999999.999999999999999999.99999999999999999"
            "----RC-SNAPSHOT.12.09.1--------------------------------..12] - "
            "1970-01-01",
            "0.0.0"
        ),

        # valid version line, but invalid changelog version lines
        (
            # missing "## " at the beginning
            "[1.2.0] - 1900-01-01", "1.2.0"
        ),
        (
            # year does not follow YYYY format
            "## [1.2.3] - 19-01-01", "1.2.3"
        ),
        (
            # month does not follow MM format
            "## [1.3.0] - 1900-1-01", "1.3.0"),
        (
            # day does not follow DD format
            "## [1.4.7] - 1900-01-1", "1.4.7"),
        (
            # month and day does not follow MM-DD form
            "## [1.5.8] - 1900-1-1", "1.5.8"),
        (
            # year, month and day does not follow YYYY-MM-DD format
            "## [1.6.0] - 19-1-1", "1.6.0"
        ),
        # there will be a problem on the first of January 10.000 :)
    )
    def test_parse_semver_line(self, line: str, expectation: str) -> None:
        """
        Test parse semver line

        :param      line:           The parse semver line
        :type       line:           str
        :param      expectation:    Expected, parsed result
        :type       expectation:    str
        """
        result = self.ev.parse_semver_line(release_version_line=line)
        self.test_logger.debug('Extracted "{}" from "{}"'.format(result, line))

        self.assertIsInstance(result, str)
        self.assertEqual(expectation, result)


if __name__ == '__main__':
    unittest.main()

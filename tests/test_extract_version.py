#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Unittest for testing the update_version file"""

import logging
from nose2.tools import params
from pathlib import Path
from sys import stdout
import unittest
from unittest.mock import patch, mock_open

from changelog2version import update_version


class TestUpdateVersion(unittest.TestCase):

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

    def tearDown(self) -> None:
        """Run after every test method"""
        pass

    def test_parse_changelog_file(self) -> None:
        """Test parse_changelog"""
        valid_changelogs_directory = self._here / 'data' / 'valid'
        valid_changelogs = [x for x in valid_changelogs_directory.iterdir()
                            if x.is_file()]

        for changelog in valid_changelogs:
            expectation = changelog.stem
            result = update_version.parse_changelog(changelog_file=changelog,
                                                    logger=self.package_logger)
            self.test_logger.debug('Extracted "{}" from "{}"'.
                                   format(result, changelog.name))

            self.assertIsInstance(result, str)
            self.assertEqual(expectation, result)

    @params(
        # valid release version lines
        ("## [0.2.0] - 2022-05-19", "0.2.0"),
        ("## [1.0.0] - 2022-07-21", "1.0.0"),
        ("## [99.42.12] - 1900-01-01", "99.42.12"),
        ("## [123456789.123456789.123456789] - 1001-01-01",
         "123456789.123456789.123456789"),
        # invalid release version lines
        ("## [1.2.c] - 1900-01-01", "0.0.0"),
        ("## [1.b.c] - 1900-01-01", "0.0.0"),
        ("## [a.b.c] - 1900-01-01", "0.0.0"),
        ("## [1.2.] - 1900-01-01", "0.0.0"),
        ("## [1.b.] - 1900-01-01", "0.0.0"),
        ("1.2.c", "0.0.0"),
        ("1.b.c", "0.0.0"),
        ("1.2.3", "0.0.0"),
        ("a.b.c", "0.0.0"),
        # valid version line, but invalid changelog version lines
        ("[1.2.0] - 1900-01-01", "0.0.0"),
        ("## [1.2.3] - 19-01-01", "0.0.0"),
        ("## [1.3.0] - 1900-1-01", "0.0.0"),
        ("## [1.4.7] - 1900-01-1", "0.0.0"),
        ("## [1.5.8] - 1900-1-1", "0.0.0"),
        ("## [1.6.0] - 19-1-1", "0.0.0"),
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
            result = update_version.parse_changelog(
                changelog_file=changelog_file,
                logger=self.package_logger)
            self.test_logger.debug('Extracted "{}" from "{}"'.
                                   format(result, changelog_file))

            self.assertIsInstance(result, str)
            self.assertEqual(expectation, result)

    @params(
        # valid release version lines
        ("## [0.2.0] - 2022-05-19", "0.2.0"),
        ("## [1.0.0] - 2022-07-21", "1.0.0"),
        ("## [99.42.12] - 1900-01-01", "99.42.12"),
        ("## [123456789.123456789.123456789] - 1001-01-01",
         "123456789.123456789.123456789"),
        # invalid release version lines
        ("## [1.2.c] - 1900-01-01", "0.0.0"),
        ("## [1.b.c] - 1900-01-01", "0.0.0"),
        ("## [a.b.c] - 1900-01-01", "0.0.0"),
        ("## [1.2.] - 1900-01-01", "0.0.0"),
        ("## [1.b.] - 1900-01-01", "0.0.0"),
        ("1.2.c", "0.0.0"),
        ("1.b.c", "0.0.0"),
        ("1.2.3", "0.0.0"),
        ("a.b.c", "0.0.0"),
        # valid version line, but invalid changelog version lines
        ("[1.2.0] - 1900-01-01", "1.2.0"),
        ("## [1.2.3] - 19-01-01", "1.2.3"),
        ("## [1.3.0] - 1900-1-01", "1.3.0"),
        ("## [1.4.7] - 1900-01-1", "1.4.7"),
        ("## [1.5.8] - 1900-1-1", "1.5.8"),
        ("## [1.6.0] - 19-1-1", "1.6.0"),
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
        result = update_version.parse_semver_line(release_version_line=line,
                                                  logger=self.package_logger)
        self.test_logger.debug('Extracted "{}" from "{}"'.format(result, line))

        self.assertIsInstance(result, str)
        self.assertEqual(expectation, result)

    @unittest.skip("Not yet implemented")
    def test_create_version_info_line(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_update_version_file(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_parse_arguments(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_parser_valid_file(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()

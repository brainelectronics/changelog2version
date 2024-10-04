#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Unittest for testing the update_version file"""

import logging
import unittest
from pathlib import Path
from sys import stdout


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

    @unittest.skip("Not yet implemented")
    def test_parser_valid_file(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_validate_regex(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_parse_arguments(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_create_version_info_line(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_update_version_file(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()

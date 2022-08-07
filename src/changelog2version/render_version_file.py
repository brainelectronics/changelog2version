#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Render version file based on template"""

from jinja2 import Environment, FileSystemLoader
import logging
from pathlib import Path
from typing import Optional, Union

from .extract_version import ExtractVersion


class RenderVersionFileError(Exception):
    """Base class for exceptions in this module."""
    pass


class RenderVersionFile(object):
    """docstring for RenderVersionFile"""
    def __init__(self,
                 template_path: Optional[Path] = None,
                 logger: Optional[logging.Logger] = None):
        """
        Init RenderVersionFile class

        :param      template_path: Path to templates
        :type       template_path: Path
        :param      logger:        Logger object
        :type       logger:        Optional[logging.Logger]
        """
        if logger is None:
            logger = ExtractVersion._create_logger()
        self._logger = logger

        self._env = None
        self._default_template_path = Path(__file__).parent / "templates"

    @property
    def default_template_path(self) -> Path:
        """
        Get path to default template folder

        :returns:   Path to template folder
        :rtype:     Path
        """
        return self._default_template_path

    @default_template_path.setter
    def default_template_path(self, template_path: Union[Path, str]) -> None:
        """
        Set path to default template folder

        :param      template_path:  The path to the template folder
        :type       template_path:  Union[Path, str]
        """
        template_path = Path(template_path)
        if template_path.exists():
            if template_path.is_dir():
                self._default_template_path = template_path
            else:
                raise RenderVersionFileError(
                    "Template path can only be a directory")
        else:
            raise RenderVersionFileError(
                "Specified directory '{}' doesn't exist".format(template_path))

    def _find_file(self, template: Union[Path, str]) -> Path:
        """
        Find template file on disk or in package templates directory

        :param      template:  The path to the template file
        :type       template:  Union[Path, str]

        :returns:   Resolved file location
        :rtype:     Path
        """
        template = Path(template)
        template_path = ""

        if template.exists():
            self._logger.debug("Template '{}' found".format(template))
            # check if file exists as the user specified it
            if template.is_file():
                template_path = template.parent
            elif template.is_dir():
                raise RenderVersionFileError(
                    "Can not render a directory, please specify a single "
                    "template file")
        elif (self.default_template_path / template).exists():
            # check if file might exist in the package templates directory
            self._logger.debug("Template '{}' found in package templates '{}'".
                               format(template, self.default_template_path))
            template = self.default_template_path / template
            if template.is_file():
                template_path = template.parent
            elif template.is_dir():
                raise RenderVersionFileError(
                    "Can not render a directory, please specify a single "
                    "template file")
        else:
            self._logger.error(
                "Template '{}' neither found in package templates directory "
                "'{}' nor at the specified path".
                format(template, self.default_template_path))
            raise RenderVersionFileError(
                "Template path/file '{}' does not exist".format(template))

        self._logger.debug("Using template path: {}".format(template_path))

        self._env = Environment(loader=FileSystemLoader(template_path),
                                keep_trailing_newline=True)

        return template.resolve()

    def render_file(self,
                    file_path: Path,
                    content: dict,
                    template: Union[Path, str]) -> None:
        """
        Render a template file with given content

        :param      file_path   The path to the file
        :type       file_path:  Path
        :param      content:    The content
        :type       content:    dict
        :param      template:   The path to the template file
        :type       template:   Union[Path, str]
        """
        template_file = self._find_file(template=template)

        content["file_name"] = file_path.name
        content["file_name_without_suffix"] = file_path.stem
        content["template_name"] = template_file.name
        content["template_name_without_suffix"] = template_file.stem

        file_template = self._env.get_template(template_file.name)
        rendered_content = file_template.render(content)

        Path(file_path.parent).mkdir(parents=True, exist_ok=True)

        if file_path.exists():
            self._logger.info("Overwriting file '{}'".format(file_path))

        with open(file_path, "w") as file:
            file.write(rendered_content)

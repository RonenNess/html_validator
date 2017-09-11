#!/usr/bin/env python
# -*- coding: utf-8 -*-

from html_validator import validate, MissingHtmlFile, ValidationError
import unittest
import os

path = os.path.dirname(os.path.realpath(__file__))
bad_filename = os.path.join(path, "test_basic_errors.html").replace('\\', '/')

# the errors we should get from the broken file
broken_file_errors = [ValidationError('''"file:/''' + bad_filename + '''":20.8-20.14: error: Stray end tag "dfiv".'''),
                      ValidationError('''"file:/''' + bad_filename + '''":21.1-21.7: error: End tag for  "body" seen, but there were unclosed elements.'''),
                      ValidationError('''"file:/''' + bad_filename + '''":20.3-20.7: error: Unclosed element "div".''')]


class TestValidate(unittest.TestCase):
    """
    Unittests to the html validator.
    """
    def test_ok_file(self):
        """
        Test validation of file with no errors.
        """
        self.assertListEqual(validate("test_no_errors.html"), [])

    def test_missing_file_exception(self):
        """
        Test validation of a missing file (exception).
        """
        self.assertRaises(MissingHtmlFile, lambda: validate("not_exist.html"))

    def test_multiple_files(self):
        """
        Test validation of multiple files.
        """
        self.assertListEqual(validate(["test_no_errors.html", "test_basic_errors.html"]), broken_file_errors)

    def test_basic_errors(self):
        """
        Test a file with some errors.
        """
        self.assertListEqual(validate(["test_basic_errors.html"]), broken_file_errors)

    def test_error_string_with_quotes(self):
        """
        Test a file with errors containing colon, to make sure it doesn't mess up parsing.
        """
        self.assertEqual(len(validate("test_basic_errors_with_colon.html")), 3)

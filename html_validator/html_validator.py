#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Wraps the v.Nu HTML validator.

Author: Ronen Ness.
Since: 2017.
"""
from __future__ import print_function
import os
import subprocess

# get the path we are in + v.Nu path
path = os.path.dirname(os.path.realpath(__file__))
vnu_path = os.path.join(path, "vnu.jar")


class ValidationError:
    """
    Represent an error we got from the HTML validator.
    """
    type = "error"          # is it warning / error / etc.
    file = ""               # filename.
    line = 0                # line number
    description = ""        # error description.
    _origin_msg = ""        # the original error message we got from v.Nu.
    
    def __init__(self, err):
        """
        Parse the error from a v.Nu error line.
        :param err: Error line from v.Nu.
                    Example: "file:/C:/projects/test.html":16.5-16.9: error: Unclosed element "div".
        """
        # remove pretty quotes (causes a useless mess)
        err = err.replace('“', '"').replace('”', '"')

        # store original error message
        self._origin_msg = err

        # get the filename part of the line, eg:
        # "file:/C:/projects/test.html"
        # from:
        # "file:/C:/projects/test.html":16.5-16.9: error: Unclosed element "div".
        filename_part = err.split('":')[0] + '"'

        # get just the filename, without the "file:" prefix or quotes. eg:
        # C:/projects/test.html
        # from:
        # "file:/C:/projects/test.html"
        self.file = filename_part.split('"file:/', 1)[-1].strip('"').strip()

        # get data without the filename part. eg:
        # 16.5-16.9: error: Unclosed element "div".
        # from:
        # "file:/C:/projects/test.html":16.5-16.9: error: Unclosed element "div".
        err_wo_filename = err[len(filename_part):].strip(':').strip()

        # get error line, eg:
        # 16
        # from:
        # "file:/C:/projects/test.html":16.5-16.9: error: Unclosed element "div".
        self.line = int(err_wo_filename.split('.')[0].strip())

        # get error type, eg:
        # error
        # from:
        # "file:/C:/projects/test.html":16.5-16.9: error: Unclosed element "div".
        self.type = err_wo_filename.split(':')[1].strip()

        # get description, eg:
        # Unclosed element "div".
        # from:
        # "file:/C:/projects/test.html":16.5-16.9: error: Unclosed element "div".
        self.description = ':'.join(err_wo_filename.split(":")[2:]).strip()

    def __repr__(self):
        return "ValidationError(%s)" % self._origin_msg

    def __str__(self):
        return "ValidationError(%s, %s, %d, %s)" % (self.type, self.file, self.line, self.description)

    def __unicode__(self):
        return unicode(str(self))

    def __eq__(self, other):
        return self._origin_msg == other._origin_msg

    def __ne__(self, other):
        return not self == other


class MissingValidatorOrJava(Exception):
    """
    Raised when Java is not properly installed, or when the jar file is missing.
    """
    def __init__(self, message):
        super(MissingValidatorOrJava, self).__init__(message)


class MissingHtmlFile(Exception):
    """
    Raised when a file to validate is missing.
    """
    def __init__(self, message):
        super(MissingHtmlFile, self).__init__(message)


def validate(files, verbose=False):
    """
    Validate a single or a list of HTML files.
    :param files: Either a single file path or a list of paths to validate.
    :param verbose: If true, will print info while processing files.
    :return: List of ValidationError with problems found in html files.
    """
    # if got a single file, convert to list
    if type(files) is not list:
        files = [files]

    # make sure all files exist
    for filename in files:
        if not os.path.exists(filename):
            raise MissingHtmlFile("Missing HTML file to test: " + filename)

    # build the command to execute
    cmd = ["java", "-Xss512k", "-jar", '%s' % vnu_path] + files
    if verbose:
        print("Execute command:", " ".join(cmd))

    # run the command to perform the validation
    try:
        # execute and get output
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if verbose:
            print("Command output:", str(output)[:256] + "...")

        # get just the errors part of the output
        errs = output[1]

    # not found on windows
    except WindowsError:
        raise MissingValidatorOrJava(
            "Got WindowsError while trying to execute command, are you sure Java is properly installed?")

    # not found on linux
    except OSError:
        raise MissingValidatorOrJava(
            "Got OSError while trying to execute command, are you sure Java is properly installed?")

    # if jar not found
    if errs is None:
        raise MissingValidatorOrJava("Couldn't get output, maybe 'vnu.jar' is missing?")

    # convert to validation error instances and return
    ret = []
    for i in errs.split('\n'):
        i = i.strip()
        if len(i) > 0:
            if verbose:
                print("Parse output line:", i)
            ret.append(ValidationError(i))

    # if verbose, print total errors found
    if verbose:
        print("Total errors found:", len(ret))

    # return errors list
    return ret

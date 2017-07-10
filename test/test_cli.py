"""
Tests for mayatest.cli

pytest
"""
import os
import mock
import pytest

from mayatest import cli
from mayatest import mayaloc


def test_args_parser_maya():
    parser = cli.args_parser(['-m', '2017'])
    assert parser.maya == 2017


def test_args_parser_pytest():
    arg = '--cov=./'
    parser = cli.args_parser(['--pytest="{0}"'.format(arg)])
    assert parser.pytest == '"{0}"'.format(arg)

    arg = 'test_module.py::test_func'
    parser = cli.args_parser(['--pytest="{0}"'.format(arg)])
    assert parser.pytest == '"{0}"'.format(arg)


def test_construct_command():
    parser = cli.args_parser(['-m', '2017', '--pytest="--cov=./"'])
    with mock.patch('os.path.isfile') as mock_isfile:
        mock_isfile.return_value = True
        cmd = cli.construct_command(parser)

    mayapy_path = mayaloc.mayapy(parser.maya)
    pytest_path = os.path.abspath(os.path.normpath(pytest.__file__))
    assert cmd == [mayapy_path, pytest_path, parser.pytest]
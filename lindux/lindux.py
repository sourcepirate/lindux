# -*- coding: utf-8 -*-

"""Main module."""

from ._base import create_index, read_line


def iread(filepath, start=0, num_lines=1):
    return read_line(filepath, start, num_lines=num_lines)


def index(filepath):
    return create_index(filepath)

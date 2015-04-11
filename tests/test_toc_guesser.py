#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path

import pytest

from ebook_serializer import guess_toc


# Functions & classes =========================================================
def data_context(fn):
    local_path = os.path.dirname(__file__)

    return os.path.join(local_path, "data", fn)


def read_data_context(fn):
    with open(data_context(fn)) as f:
        return f.read()


@pytest.fixture
def toc_example():
    return read_data_context("toc_example.html")


@pytest.fixture
def toc_links():
    return read_data_context("toc_links.txt").splitlines()


# with pytest.raises(Exception):
#     raise Exception()


# Tests =======================================================================
def test_guess_toc(toc_example):
    toc = guess_toc(toc_example)

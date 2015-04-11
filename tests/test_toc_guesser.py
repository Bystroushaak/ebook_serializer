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


@pytest.fixture
def toc_example():
    with open(data_context("toc_example.html")) as f:
        return f.read()

# with pytest.raises(Exception):
#     raise Exception()


# Tests =======================================================================
def test_guess_toc(toc_example):
    pass

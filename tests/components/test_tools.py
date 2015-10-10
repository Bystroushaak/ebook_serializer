#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from ebook_serializer.components.tools import to_absolute_url
from ebook_serializer.components.tools import links_to_absolute_url

from ..test_toc_guesser import toc_links
from ..test_toc_guesser import read_data_context


# Variables ===================================================================
BASE_URL = "http://pharo.gemtalksystems.com"


# Fixtures ====================================================================
@pytest.fixture
def abs_toc_links():
    return read_data_context("absolute_toc_links.txt").splitlines()


# Tests =======================================================================
def test_to_absolute_url():
    absolute_url = "http://pharo.gemtalksystems.com/book/table-of-contents/"
    relative_url = "./book/table-of-contents/"  # notice the ./

    assert absolute_url == to_absolute_url(
        relative_url,
        base_url=BASE_URL
    )


def test_links_to_absolute_url(toc_links, abs_toc_links):
    abs_links = links_to_absolute_url(toc_links, base_url=BASE_URL)

    assert abs_links == abs_toc_links

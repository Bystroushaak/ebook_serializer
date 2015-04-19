#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from ebook_serializer import book_constructor

from test_toc_guesser import toc_links


# Variables ===================================================================



# Fixtures ====================================================================



# Tests =======================================================================
def test_to_absolute_url(toc_links):
    absolute_url = "http://pharo.gemtalksystems.com/book/table-of-contents/"
    base_url = "http://pharo.gemtalksystems.com"
    relative_url = "./book/table-of-contents/"  # notice the ./

    assert absolute_url == book_constructor._to_absolute_url(
        relative_url,
        base_url
    )

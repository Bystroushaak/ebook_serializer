#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path

import pytest
import dhtmlparser

from ebook_serializer import toc_guesser


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


# Tests =======================================================================
def test_number_of_links():
    dom = dhtmlparser.parseString(
        """
        <root>
            <a />
            <sub>
                <a />
            </sub>
        </root>
        """
    )

    assert toc_guesser._number_of_links(dom) == 2
    assert toc_guesser._number_of_links(dom.find("sub")[0]) == 1


def test_parent_iterator():
    dom = dhtmlparser.parseString(
        """
        <root>
            <a />
            <sub>
                <a attr=1 />
            </sub>
        </root>
        """
    )
    dhtmlparser.makeDoubleLinked(dom)

    a_tag = dom.find("a", {"attr": "1"})[0]
    assert a_tag

    parents = list(toc_guesser._parent_iterator(a_tag))
    assert parents

    assert parents == [
        dom.find("sub")[0],
        dom.find("root")[0],
        dom
    ]


def test_identify_jump():
    test_set = [
        (1, None),
        (5, None),
        (50, "here"),
        (51, None),
        (54, None),
    ]

    assert toc_guesser._identify_jump(test_set) == "here"


def test_guess_toc_element(toc_example):
    toc = toc_guesser.guess_toc_element(toc_example)
    dom = dhtmlparser.parseString(toc_example)

    assert toc.__str__() == dom.find("dl")[0].__str__()


def test_guess_toc_links(toc_example, toc_links):
    assert toc_guesser.guess_toc_links(toc_example) == toc_links

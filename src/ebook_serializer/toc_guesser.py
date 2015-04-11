#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser


# Variables ===================================================================



# Functions & classes =========================================================
def _number_of_links(el):
    return len(el.find("a"))


def guess_toc(document):
    dom = dhtmlparser.parseString(document)
    dhtmlparser.makeDoubleLinked(dom)

    links = dom.find("a")

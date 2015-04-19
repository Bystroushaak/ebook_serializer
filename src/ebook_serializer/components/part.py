#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class Part(object):
    def __init__(self, *args):
        self.chapters = args

    def _deep_download(self, book_ref):
        for chapter in self.chapters:
            chapter._deep_download(book_ref)

#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Variables ===================================================================
# Functions & classes =========================================================
class Book(object):
    def __init__(self):
        self.title = None
        self.sub_title = None
        self.author = None

        self.isbn = None
        self.publisher = None
        self.year = None

        self._chapters = []

    def add_chapter(self, chapter):
        self._chapters.append(chapter)

    def serialize(self, path):
        pass

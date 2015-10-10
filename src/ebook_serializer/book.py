#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import components

# Variables ===================================================================
# Functions & classes =========================================================
class Book(object):
    def __init__(self):
        self.chapters = []
        self.images = {}

        # required metadata
        self.title = None
        self.author = None
        self.sub_title = None

        # optional metadata
        self.isbn = None
        self.year = None
        self.publisher = None

        self.cover = None


class EpubBook(Book):
    def __init__(self):
        super(EpubBook, self).__init__()

    def to_epub(self):
        pass

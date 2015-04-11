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

    def serialize(self, dir_path):
        for chapter in self.chapters:
            chapter.serialize(dir_path)

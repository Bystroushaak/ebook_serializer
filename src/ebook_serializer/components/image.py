#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import hashlib


# Variables ===================================================================
# Functions & classes =========================================================
class Image(object):
    def __init__(self, content, filename=None):
        self.content = content
        self.filename = filename

    def get_filename(self):
        if self.filename:
            return self.filename

        return hashlib.md5(self.content).hexdigest()  # TODO: suffix from mime

#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from .chapter import Chapter


# Variables ===================================================================
# Functions & classes =========================================================
class MicroChapter(Chapter):
    def __init__(self, html):
        super(MicroChapter, self).__init__(html)

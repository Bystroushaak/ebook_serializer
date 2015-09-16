#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import hashlib
import unicodedata

import dhtmlparser


# Variables ===================================================================
# Functions & classes =========================================================
class Chapter(object):
    def __init__(self, url, content=None, title=None, filename=None):
        self.title = title
        self.content = content
        self.url = url

        self._suffix = ".html"
        self.filename = filename

        try:
            self.dom = dhtmlparser.parseString(content)
        except UnicodeDecodeError:
            self.dom = dhtmlparser.parseString(content.encode("utf-8"))

    def _deep_download(self, book_ref):
        pass

    def get_title(self):
        if self.title is not None:
            return self.title

        headings = []
        headings.extend(self.dom.find("h1"))
        headings.extend(self.dom.find("h2"))
        headings.extend(self.dom.find("h3"))
        headings.extend(self.dom.find("h4"))
        headings.extend(self.dom.find("h5"))
        headings.extend(self.dom.find("h6"))

        for h in headings:
            heading_content = dhtmlparser.removeTags(h.getContent())
            heading_content = heading_content.strip()

            # remove unnecessary spaces
            heading_content = " ".join(heading_content.split())

            if heading_content:
                return heading_content

    def _safe_filename(self, fn):
        fn = fn.decode("utf-8")
        fn = unicodedata.normalize('NFKD', fn).encode('ascii', 'ignore')
        fn = fn.replace(" ", "_")

        return "".join(
            char
            for char in fn
            if char.isalnum() or char in ".-_"
        )

    def get_filename(self):
        if self.filename is not None:
            return self.filename

        title = self.get_title()

        if title:
            return self._safe_filename(title) + self._suffix

        return hashlib.md5(self.content).hexdigest() + self._suffix

    def __repr__(self):
        return self.get_filename()

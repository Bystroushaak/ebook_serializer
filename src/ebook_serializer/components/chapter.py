#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import hashlib

import dhtmlparser

from tools import safe_filename


# Variables ===================================================================
# Functions & classes =========================================================
class Chapter(object):
    def __init__(self, title, content, filename=None):
        self.title = title
        self.content = content
        self.filename = filename

        self._suffix = ".txt"


class HTMLChapter(Chapter):
    def __init__(self, title=None, content=None, filename=None, url=None):
        super(HTMLChapter, self).__init__(
            title=title,
            content=content,
            filename=filename,
        )

        self.url = url
        self._suffix = ".html"

        try:
            self.dom = dhtmlparser.parseString(content)
        except UnicodeDecodeError:
            self.dom = dhtmlparser.parseString(content.encode("utf-8"))

    def process_linked_elements(self, process_image, process_link):
        for img in self.dom.find("img"):
            process_image(img)

        for link in self.dom.find("a", fn=lambda x: "href" in x.params):
            process_link(link)

        # for style in # TODO: implement later

    @property
    def title(self):
        if self.__dict__.get("title") is not None:
            return self.__dict__["title"]

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

    @title.setter
    def title(self, new_title):
        self.__dict__["title"] = new_title

    @property
    def filename(self):
        if self.filename is not None:
            return self.filename

        if self.title:
            return safe_filename(self.title) + self._suffix

        return hashlib.md5(self.content).hexdigest() + self._suffix

    @filename.setter
    def filename(self, new_filename):
        self.__dict__["filename"] = new_filename

    # TODO: ABC method
    def postprocess_content(self):
        return self.dom.__str__()

    @property
    def content(self):
        return self.postprocess_content()

    def __repr__(self):
        return self.filename

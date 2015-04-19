#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import requests

import components


# Variables ===================================================================
# Functions & classes =========================================================
class Book(object):
    def __init__(self, toc_links, base_url):
        self.title = None
        self.sub_title = None
        self.author = None

        self.isbn = None
        self.publisher = None
        self.year = None

        self._chapters = []
        self.toc_links = toc_links
        self.base_url = base_url

        self._construct_book()

    def _construct_book(self):
        for link in self.toc_links:
            content = self.download(link)

            self.add_chapter(
                self.type_decisioner(content)
            )

        self._deep_download()

    def download(self, url):
        return requests.get(url)

    def type_decisioner(self, content):
        return components.Chapter(content)

    def add_chapter(self, chapter):
        self._chapters.append(chapter)

    def _deep_download(self):
        for chapter in self._chapters:
            chapter._deep_download(self)
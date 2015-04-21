#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from urlparse import urljoin

import requests

import components


# Variables ===================================================================
# Functions & classes =========================================================
def _to_absolute_url(link, base_url):
    if link.startswith("http://") or link.startswith("https://"):
        return link

    return urljoin(base_url, link)


def _links_to_absolute_url(links, base_url):
    return [
        _to_absolute_url(link, base_url)
        for link in links
    ]


class Book(object):
    def __init__(self, toc_links, base_url):
        self.title = None
        self.author = None
        self.sub_title = None

        self.isbn = None
        self.year = None
        self.publisher = None

        self.base_url = base_url
        self.toc_links = toc_links

        self._urls = {}  #: url:Chapter mappings to avoid redownload
        self._chapters = []

    def download_book(self):
        for link in self.toc_links:
            self.add_chapter(link)

        self._deep_download()

    def _deep_download(self):
        for chapter in self._chapters:
            chapter._deep_download(self)

    def add_chapter(self, url, chapter=None):
        url = _to_absolute_url(url, self.base_url)

        if url in self._urls:
            return

        if not chapter:
            content = self.download(url)
            chapter = self.type_decisioner(content, url)

        self._urls[url] = chapter
        self._chapters.append(chapter)

    def download(self, url):
        return requests.get(url).text.encode("utf-8")

    def type_decisioner(self, content, url):
        print url
        return components.Chapter(content)

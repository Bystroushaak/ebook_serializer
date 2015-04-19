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


def links_to_absolute_url(links, base_url):
    return [
        _to_absolute_url(link, base_url)
        for link in links
    ]


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

            content_type = self.type_decisioner(content)

            self.add_chapter(
                content_type(content)
            )

    def download(self, url):
        return requests.get(url)

    def type_decisioner(self, content):
        return components.Chapter

    def content_trimmer(self, content):
        return content

    def add_chapter(self, chapter):
        self._chapters.append(chapter)

    def deep_download(self, base_url, type_decisioner, content_trimmer,
                      downloader):
        for chapter in self._chapters:
            chapter.deep_download(
                base_url=base_url,
                type_decisioner=type_decisioner,
                content_trimmer=content_trimmer,
                downloader=downloader
            )

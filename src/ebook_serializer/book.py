#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import components

import shared

# Variables ===================================================================
_BOOK_CACHE = None


# Functions & classes =========================================================
class Book(object):
    def __init__(self, base_url, toc_links=[], chapters=[]):
        # required metadata
        self.title = None
        self.author = None
        self.sub_title = None

        # optional metadata
        self.isbn = None
        self.year = None
        self.publisher = None

        self.cover = None

        # internal parts
        self.base_url = base_url
        self.toc_links = toc_links

        self._urls = {}  #: url:Chapter mappings to avoid redownloads
        self.chapters = chapters

    def download_book(self):
        for link in self.toc_links:
            self.add_chapter_by_url(link)

        self._deep_download()

    def _deep_download(self):
        for chapter in self.chapters:
            chapter._deep_download()

    def add_chapter_by_url(self, url):
        url = shared.to_absolute_url(url, self.base_url)

        if url in self._urls:
            return

        chapter = components.Chapter(
            url=url,
            content=shared.download(url),
        )

        self.add_chapter_by_obj(chapter)

    def add_chapter_by_obj(self, chapter):
        self._urls[chapter.url] = chapter
        self.chapters.append(chapter)


def book(*args, **kwargs):
    """
    Make sure, that Book is singleton.
    """
    if not _BOOK_CACHE:
        global _BOOK_CACHE
        _BOOK_CACHE = Book(*args, **kwargs)

    return _BOOK_CACHE

#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import hashlib
import urlparse

import dhtmlparser

from tools import https_url
from tools import safe_filename


# Variables ===================================================================
# Functions & classes =========================================================
class Chapter(object):
    def __init__(self, title, content, filename):
        self.title = title
        self.content = content
        self.filename = filename

        self._suffix = ".txt"


class HTMLChapter(Chapter):
    def __init__(self, base_url, title=None, content=None, filename=None,
                 url=None, lazy=False):
        super(HTMLChapter, self).__init__(
            title=title,
            content=content,
            filename=filename,  # may be None, fixed later by property
        )

        self.url = url
        self.base_url = base_url

        self._suffix = ".html"

        self.dom = None
        self.cropped_content = None
        self.cropped_dom = None

        if not lazy:
            self.parse()

    def parse(self):
        try:
            self.dom = dhtmlparser.parseString(self.content)
        except UnicodeDecodeError:
            self.content = self.content.encode("utf-8")
            self.dom = dhtmlparser.parseString(self.content)

        self.cropped_content = self.crop_content(
            content=self.content,
            dom=self.dom
        )
        self.cropped_dom = dhtmlparser.parseString(self.cropped_content)

    def crop_content(self, content, dom):
        body = dom.find("body")

        if not body:
            return content

        return body[0].getContent()

    def link_on_banlist(self, link):
        if not (link.startswith(self.base_url) or
                link.startswith(https_url(self.base_url))):
            return True

        suffix = link.rsplit(".")[-1]
        if suffix in {"zip", "rar", "gz", "tar"}:
            return True

        return False

    def _to_absolute_url(self, link):
        if "://" in link:
            return link

        return urlparse.urljoin(self.base_url, link)

    def find_links(self):
        all_links = (
            self._to_absolute_url(link.params["href"])
            for link in self.dom.find("a")
            if link.params.get("href", None)
        )

        # filter links on banlist
        return [
            link
            for link in all_links
            if not self.link_on_banlist(link)
        ]

    def _find_images(self):
        return [
            self._to_absolute_url(img.params["src"])
            for img in self.dom.find("img")
            if img.params.get("src", None)
        ]

    def _find_styles(self):
        style_elements = [
            self._to_absolute_url(style.params["href"])
            for style in self.dom.find("style")
            if "href" in style.params
        ]

        link_elements = [
            self._to_absolute_url(style.params["href"])
            for style in self.dom.find("link", {"rel": "stylesheet"})
            if "href" in style.params
        ]

        link_elements2 = [
            self._to_absolute_url(style.params["href"])
            for style in self.dom.find("link", {"type": "text/css"})
            if "href" in style.params
        ]

        return style_elements + link_elements + link_elements2

    @property
    def title(self):
        if self.__dict__.get("title") is not None:
            return self.__dict__["title"]

        headings = []
        headings.extend(self.dom.find("title"))
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

    def __repr__(self):
        return self.filename

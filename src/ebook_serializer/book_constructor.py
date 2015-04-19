#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from urlparse import urljoin

import requests

from ebook_serializer import toc_guesser

from components import book


# Variables ===================================================================



# Functions & classes =========================================================
def _to_absolute_url(link, base_url):
    if link.startswith("http://") or link.startswith("https://"):
        return link

    return urljoin(base_url, link)


def _links_to_absolute_url(links, base_url):
    return (
        _to_absolute_url(link, base_url)
        for link in links
    )


def construct_book(toc_links, base_url):
    toc_links = _links_to_absolute_url(toc_links, base_url)

    for link in toc_links:
        content = requests.get(link)

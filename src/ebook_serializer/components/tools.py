#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import unicodedata
from urlparse import urljoin

import requests


# Variables ===================================================================
# Functions & classes =========================================================
def to_absolute_url(link, base_url):
    if link.startswith("http://") or link.startswith("https://"):
        return link

    return urljoin(base_url, link)


def links_to_absolute_url(links, base_url):
    return [
        to_absolute_url(link, base_url)
        for link in links
    ]


def download(url):
    return requests.get(url).text.encode("utf-8")


def safe_filename(fn):
    fn = fn.decode("utf-8")
    fn = unicodedata.normalize('NFKD', fn).encode('ascii', 'ignore')
    fn = fn.replace(" ", "_")

    return "".join(
        char
        for char in fn
        if char.isalnum() or char in ".-_"
    )

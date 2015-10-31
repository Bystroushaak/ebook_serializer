#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import shutil
import os.path
import tempfile
from os.path import join

import components


# Variables ===================================================================
# Functions & classes =========================================================
class Book(object):
    def __init__(self):
        self.images = {}
        self.styles = {}
        self.chapters = []

        # required metadata
        self.title = None
        self.authors = []
        self.sub_title = None
        self.language = "en"

        # optional metadata
        self.isbn = None
        self.published = None
        self.publisher = None
        self.source = None

        self.cover = None


class EpubBook(Book):
    def __init__(self):
        super(EpubBook, self).__init__()

        self._tmp_dir = None

    def _create_mime(self):
        """
        Create mimetype file to identify ZIP as epub.
        """
        mimetype_fn = join(self._tmp_dir, "mimetype")

        with open(mimetype_fn, "w") as f:
            f.write("application/epub+zip")

    def _create_meta_inf(self):
        """
        Create meta information file pointing to content file.
        """
        meta_inf_path = join(self._tmp_dir, "META-INF")
        container_fn = join(meta_inf_path, "container.xml")

        os.mkdir(meta_inf_path)

        with open(container_fn, "w") as f:
            f.write("""<?xml version="1.0" encoding="utf-8"?>
<container version="1.0"
           xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
              media-type="application/oebps-package+xml" />
  </rootfiles>
</container>""")

    def _process_content(self):
        pass

    def _create_cover(self):
        pass

    def _create_toc_ncx(self):
        # TODO: cover
        pass

    def _create_content_opf(self):
        pass

    def _create_oebps(self):
        oebps_path = join(self._tmp_dir, "OEBPS")

        os.mkdir(oebps_path)
        self._process_content()

        if self.cover:
            self._create_cover()

        self._create_toc_ncx()
        self._create_content_opf()

    def to_epub(self):
        self._tmp_dir = tempfile.mkdtemp()

        self._create_mime()
        self._create_meta_inf()
        self._create_oebps()

        # TODO: zip everything

        # temporary directory cleanup
        # shutil.rmtree(self._tmp_dir)
        return self._tmp_dir  # TODO: remove

        # return zip_content

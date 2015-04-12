#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser


# Functions & classes =========================================================
def cached(fn):
    """
    Cache decorator. This decorator simply uses ``*args`` as lookup key for
    cache dict.

    If you are using python3, use functools.lru_cache() instead.
    """
    cache = {}

    def cached_decorator(*args, **kwargs):
        if args in cache:
            return cache[args]

        val = fn(*args, **kwargs)
        cache[args] = val

        return val

    return cached_decorator


@cached
def _number_of_links(el):
    """
    Count number of links in `el`.

    Note:
        This function is cached. See :func:`cached` for details.

    Args:
        el (obj): HTMLElement instance.

    Returns:
        int: Number of occurences of ``<a>`` tag in `el`.
    """
    return len(el.find("a"))


def _parent_iterator(el):
    """
    Iterate thru ``.parent`` properties in double linked element tree.

    Args:
        el (obj): HTMLElement instance in double linked list.

    Raises:
        AttributeError: If `el` is not from double linked list.

    Yeilds:
        All parent elements.
    """
    while el.parent:
        yield el.parent
        el = el.parent


def _identify_jump(elements):
    """
    Indetify jump in list of pairs ``[num, el]``. Jump is defined as highest
    derivation of `num`.

    Args:
        elements (list of tuples): List of tuples, where first item is number.

    Returns:
        obj: `el` from the pair with highest derivation. See tests for details.
    """
    # perform numerical derivation of items in clusters
    old = 0
    jumps = []
    for num, el in elements:
        jumps.append(
            (num - old, el)
        )
        old = num

    # pick item with highest derivation
    return max(jumps, key=lambda x: x[0])[1]


def guess_toc_element(document):
    """
    For given `document`, guess which HTMLElement holds TOC (Table Of Content).

    This function picks most used cluster with highest derivation of ``<a>``
    element count.

    Args:
        document (str): Document which should contain TOC somewhere.

    Returns:
        obj: HTMLelement instance which looks like it *may* contain TOC.
    """
    dom = dhtmlparser.parseString(document)
    dhtmlparser.makeDoubleLinked(dom)

    links = dom.find("a")

    # construct parent tree
    tree = {}
    for link in links:
        tree[link] = []

        for parent in _parent_iterator(link):
            num_of_links = _number_of_links(parent)

            tree[link].append(
                (num_of_links, parent)
            )

    # find biggest jumps in number of elements in <a> clusters
    jumps = {}
    for link in links:
        jump = _identify_jump(tree[link])

        jumps[jump] = jumps.get(jump, 0) + 1

    # pick element containing most links
    return max(jumps, key=lambda x: jumps[x])


def guess_toc_links(document):
    """
    Look for TOC, return list of (relative) links from element which looks like
    TOC.

    Args:
        document (str): Document which should contain TOC somewhere.

    Returns:
        list: List of links from element which looks like it *may* contain TOC.
    """
    toc_element = guess_toc_element(document)

    return [
        link.params["href"].replace("&amp;", "&")
        for link in toc_element.find("a")
        if "href" in link.params
    ]

#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser


# Functions & classes =========================================================
def cached(fn):
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
    return len(el.find("a"))


def _parent_iterator(el):
    while el.parent:
        yield el.parent
        el = el.parent


def _identify_jump(elements):
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
    toc_element = guess_toc_element(document)

    return [
        link.params["href"].replace("&amp;", "&")
        for link in toc_element.find("a")
        if "href" in link.params
    ]

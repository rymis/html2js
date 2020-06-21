#!/usr/bin/env python3

"""
HTML DOM implementation for Python.
"""

import html.parser

class Node:
    pass

class DeclNode(Node):
    """ Declaration node like <?DOCTYPE html> """
    def __init__(self, content, position = None):
        self.content = content
        self.position = position

    def to_html(self):
        return f"<!{self.content}>"

class TextNode(Node):
    """ Textual node representation """
    def __init__(self, text, position = None):
        self.text = text
        self.position = position

    def to_html(self):
        return self.text

class Element(Node):
    """ Regular HTML element representaion """
    def __init__(self, tag, attrs = None, children = None, root_element = False, position = None):
        self.tag = tag
        self.attrs = {}
        self.children = []
        self.position = position
        self.root_element = root_element
        if attrs:
            for key, value in attrs:
                self.attrs[key] = value
        if children:
            self.children.extend(children)

    def to_html(self):
        res = [ f"<{self.tag}" ]
        for nm, v in self.attrs.items():
            res.append(f' {nm}="{v}"')
        res.append(">")
        if self.root_element:
            res = []
        for c in self.children:
            res.append(c.to_html())
        if not self.root_element:
            res.append(f"</{self.tag}>")
        return "".join(res)


class _P(html.parser.HTMLParser):
    AUTOCLOSE = set([ "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr", "command", "keygen", "menuitem" ])

    def __init__(self):
        super().__init__()
        self._stack = [ Element("root-element", root_element = True) ]

    def handle_starttag(self, tag, attrs):
        self._stack.append(Element(tag, attrs, position = self.getpos()))

    def _append_last(self):
        self._stack[-2].children.append(self._stack[-1])
        self._stack.pop()

    def handle_endtag(self, tag):
        while len(self._stack) > 1 and self._stack[-1].tag != tag:
            self._append_last()
        if len(self._stack) > 1 and self._stack[-1].tag == tag:
            self._append_last()

    def handle_data(self, data):
        self._stack[-1].children.append(TextNode(data, position = self.getpos()))

    def handle_decl(self, content):
        self._stack[-1].children.append(DeclNode(content, position = self.getpos()))

    def dom(self):
        return self._stack[0]

def parse_html(file_or_name):
    if isinstance(file_or_name, str):
        with open(file_or_name) as f:
            return parse_html(f)
    p = _P()
    p.feed(file_or_name.read())

    return p.dom()


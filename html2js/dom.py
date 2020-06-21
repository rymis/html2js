#!/usr/bin/env python3

"""
HTML DOM implementation for Python.
"""

import html.parser
import json
from . import text

class Node:
    def to_html(self):
        " Show element as HTML "
        raise NotImplemented

    def generate(self, context):
        " Generate JS code "
        raise NotImplemented

    def generate_js(self, nm):
        raise NotImplemented

class DeclNode(Node):
    """ Declaration node like <?DOCTYPE html> """
    def __init__(self, content, position = None):
        self.content = content
        self.position = position

    def to_html(self):
        return f"<!{self.content}>"

    def generate(self, ctx):
        ctx.add_text(f"<!{self.content}>", raw = True)

_LAST_TMP = 0
def _tmp_name():
    global _LAST_TMP
    _LAST_TMP += 1
    return f"__t{_LAST_TMP}"

class TextNode(Node):
    """ Textual node representation """
    def __init__(self, text, position = None):
        self.text = text
        self.position = position

    def to_html(self):
        return self.text

    def generate(self, ctx):
        ctx.add_text(self.text)

    def generate_js(self, nm):
        res = [ ]
        txt = text.parse_text(self.text)
        for t in txt:
            if isinstance(t, str):
                res = f"{nm}.appendChild(document.createTextNode({json.dumps(t)}));"
            else:
                res = f"{nm}.appendChild(this._createTextNode({t.path}));"

class Element(Node):
    """ Regular HTML element representaion """
    def __init__(self, tag, attrs = None, children = None, position = None, autoclose = False):
        self.tag = tag
        self.attrs = {}
        self.children = []
        self.position = position
        self.root_element = tag == "root-element"
        self.autoclose = autoclose
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

    def generate(self, ctx):
        ctx.start_tag(self.tag, self.attrs)
        for c in self.children:
            c.generate(ctx)
        if not self.autoclose:
            ctx.end_tag(self.tag)

    def generate_js(self, nm):
        pass

_CUSTOM_ELEMENTS = { }

def custom(tag):
    """\
Decorator which allows to define custom elements.

Decorated class should be a subclass of Element.
"""
    def decorator(cls):
        assert issubclass(cls, Element)
        _CUSTOM_ELEMENTS[tag] = cls
        return cls
    return decorator

@custom("if")
class IfElement(Element):
    def generate(self, ctx):
        pass

@custom("else")
class ElseElement(Element):
    def generate(self, ctx):
        pass

@custom("for")
class ForElement(Element):
    def generate(self, ctx):
        pass

def _create_element(tag, attrs, position, autoclose = False):
    cls =  _CUSTOM_ELEMENTS.get(tag, Element)
    return cls(tag, attrs, position = position, autoclose = autoclose)

class _P(html.parser.HTMLParser):
    AUTOCLOSE = set([ "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr", "command", "keygen", "menuitem" ])

    def __init__(self):
        super().__init__()
        self._stack = [ Element("root-element") ]

    def handle_starttag(self, tag, attrs):
        if tag in self.AUTOCLOSE:
            self._stack[-1].children.append(_create_element(tag, attrs, self.getpos(), autoclose = True))
        else:
            self._stack.append(_create_element(tag, attrs, self.getpos()))

    def _append_last(self):
        self._stack[-2].children.append(self._stack[-1])
        self._stack.pop()

    def handle_endtag(self, tag):
        if tag in self.AUTOCLOSE:
            return

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


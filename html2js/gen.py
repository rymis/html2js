#!/usr/bin/env python3

import html

__doc__ = """\
Generator context for html2js
"""

class Generator:
    def __init__(self):
        self.out = []

    def start_tag(self, tag, attrs):
        self.out.append("<%s%s>" % (tag, "".join([' %s="%s"' % (nm, html.escape(val) for nm, val in attrs.items())])))

    def end_tag(self, tag):
        self.out.append("</%s>" % tag)

    def add_text(self, text, raw = False):
        if raw:
            self.out.append(text)
        else:
            self.out.append(html.escape(text))

    def get_page(self):
        return "".join(self.out)


#!/usr/bin/env python3

import re

# Simple template text parser
_REGEX = re.compile(r"\{\{[^}]*\}\}")

__doc__ = """Text parser for html2js package.

Supported constructions in text are:
    1. name - this is a field of the returned object.
    2. name.name2... - in returned object will be created subobject with name 'name' and field 'name2' in this subobject.
"""

class Entry:
    def __init__(self, path):
        self.path = path
        self._parsed = self._parse(path)

    def _parse(self, s):
        return [ x.strip() for x in s.split('.') ]

    def __repr__(self):
        return f"Entry({self.path})"

def parse_text(text):
    last_pos = 0
    parts = []
    for x in _REGEX.finditer(text):
        pos, endpos = x.span()
        if pos > last_pos:
            parts.append(text[last_pos:pos])
            last_pos = endpos
        parts.append(Entry(x.group(0)))
    if len(text) > last_pos:
        parts.append(text[last_pos:])

    print(parts)

if __name__ == '__main__':
    print(_REGEX.match("{{test['123']}}"))

    parse_text('text{{var.field[}}text2')

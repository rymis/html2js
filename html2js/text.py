#!/usr/bin/env python3

import re

# Simple template text parser
_REGEX = re.compile(r"\{\{[^}]*\}\}")

class Entry:
    def __init__(self, path):
        self.path = path

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

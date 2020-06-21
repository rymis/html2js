#!/usr/bin/env python3

import argparse
from . import dom

def main():
    args = argparse.ArgumentParser(description = "Compile HTML into JavaScript application")
    aa = args.add_argument
    aa("inputs", nargs = 1, help = "Input file")
    aa("-o", "--output", help = "Output file name (default input_name.js)")
    opts = args.parse_args()

    filename = opts.inputs[0]
    html = dom.parse_html(filename)
    print(html.to_html())

main()

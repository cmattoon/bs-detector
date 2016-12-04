#!/usr/bin/env python
"""
Digests a text file of links in the format:

link.com[,reason]

And adds them to data.json in alphabetical order.

Usage:
./scripts/add_links.py <path/to/input.txt> [path/to/data.json]
"""
import os
import json
import sys

# change to (e.g., 2) for pretty-print
INDENT = None

DATA_FILES = [
    'chrome/data/data.json',
    'firefox/data/data.json'
]

def get_links(filename):
    """
    Returns a dict of {url: reason}
    """
    urls = {}
    with open(filename, 'rb') as fd:
        lines = [line.strip() for line in fd.readlines() if line.strip()]

    for line in lines:
        line = line.split(',')

        try:
            urls[line[0]] = line[1]
        except IndexError:
            urls[line[0]] = ''

    return urls

def add_links(links, datafile):
    """Adds a dict of links to `datafile`

    Args:
      links dict {url: reason}
      datafile string path to file
    """
    with open(datafile, 'rb') as fd:
        data = fd.read()

    data = json.loads(data)

    for url in links:
        data.append({"url": url, "type": links[url]})

    # Remove duplicates
    seen = {}
    for i, obj in enumerate(data):
        try:
            x = seen[obj['url']]
            print("Duplicate: %s" % (obj['url']))
            del data[i]
        except KeyError:
            seen[obj['url']] = True

    data = sorted(data, key=lambda k: k['url'])

    with open(datafile, 'wb') as fd:
        json.dump(data, fd, indent=None)

if __name__ == '__main__':
    infile = os.path.abspath(sys.argv[1])

    for outfile in DATA_FILES:
        add_links(get_links(infile), outfile)

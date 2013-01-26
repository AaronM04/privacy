#!/usr/bin/python
#
VERSION_STRING='2013-01-21 13:45'
#
# extract_chrome_dns_urls.py - when given a saved HTML document from
#   'chrome://dns', extract all the URLs (http and https protocols) that are
#   present, sort them in DNS (top-level domain then lower levels) order, and
#   print to standard output.  With the --hosts flag, prepend each line with
#   '127.0.0.1' and some whitespace for /etc/hosts blocking.  The purpose of this
#   is to block ads and tracking sites.

import sys
import re
from getopt import getopt, GetoptError
from HTMLParser import HTMLParser

all_data = []

def handle_data_factory():
    """Produces a function that can be called to save the data to a list.
    Returns a tuple of (<handle_data function>, all_data)."""
    all_data = list()
    def handle_data(data):
        all_data.append(data)
    return (handle_data, all_data)

if __name__ == '__main__':
    f = sys.stdin

    # TODO: get options

    s = sys.stdin.read()

    # handle_data is a function which appends its argument to the all_data list
    handle_data, all_data = handle_data_factory()

    parser = HTMLParser()
    parser.handle_data = handle_data
    parser.feed(s)

    all_urls = filter(lambda x: re.match(r'^https?://', x), all_data)
    all_urls = list(set(all_urls))

#!/usr/bin/python
#
VERSION_STRING='2013-01-26 15:15'
#
# extract_chrome_dns_urls.py - when given a saved HTML document from
#   'chrome://dns', extract all the URLs (http and https protocols) that are
#   present, sort them in DNS (top-level domain then lower levels) order, and
#   print to standard output.  With the --hosts flag, strip everything but the
#   domain, prepend each line with '127.0.0.1' and some whitespace for
#   /etc/hosts blocking.  The purpose of this is to block ads and tracking
#   sites.

import sys
import re
from getopt import getopt, GetoptError
from HTMLParser import HTMLParser

def handle_data_factory():
    """Produces a function that can be called to save the data to a list.
    Returns a tuple of (<handle_data function>, all_data)."""
    all_data = list()
    def handle_data(data):
        all_data.append(data)
    return (handle_data, all_data)



def url_to_dom(url):
    """Convert a URL to a raw domain (e.g., 'http://www.google.com/' becomes
    'www.google.com')"""
    return url.rstrip('/').split('//')[-1]



def cmp_dns_order(url_x, url_y):
    """Compare the two URLs in 'DNS order', meaning the the top level domains
    are sorted ASCII-betically, then the next-highest, then the next, etc.
    Returns one of {-1, 0, 1} like cmp()."""

    dom_x = url_to_dom(url_x)
    dom_y = url_to_dom(url_y)

    revdom_x = '.'.join(reversed(dom_x.split('.')))
    revdom_y = '.'.join(reversed(dom_y.split('.')))

    return cmp(revdom_x, revdom_y)



if __name__ == '__main__':
    output_hosts_fmt = False

    f = sys.stdin

    opts, args = getopt(sys.argv[1:], '', ['hosts'])
    for longopt, opt in opts:
        if longopt == '--hosts':
            output_hosts_fmt = True

    if len(args) > 1:
        print >>sys.stderr, "ERROR: too many arguments"
        sys.quit(1)

    if len(args) == 1:
        in_file = args[0]
        try:
            f = file(in_file, 'r')    # replaces sys.stdin (see above)
        except IOError, e:
            print >>sys.stderr, "ERROR: could not open file %r: %r" % (in_file, e)
            sys.quit(1)

    s = f.read()

    # handle_data is a function which appends its argument to the all_data list
    handle_data, all_data = handle_data_factory()

    parser = HTMLParser()
    parser.handle_data = handle_data
    parser.feed(s)

    # extract everything that looks like a URL
    all_urls = filter(lambda x: re.match(r'^https?://', x), all_data)

    # remove duplicates and sort in DNS order
    all_urls = list(set(all_urls))
    all_urls = sorted(all_urls, cmp=cmp_dns_order)

    if output_hosts_fmt:        # --hosts
        entries = []
        for url in all_urls:
            dom = url_to_dom(url)
            entries.append('127.0.0.1   ' + dom)
        print '\n'.join(entries)
    else:
        print '\n'.join(all_urls)

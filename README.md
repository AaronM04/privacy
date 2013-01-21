Aaron's Privacy Tools
-------------

This is (or will be) a very diverse group of tools for improving or managing privacy.

### extract_chrome_dns_urls.py

When given a saved HTML document from 'chrome://dns', extract all the URLs (http and https protocols) that are present, sort them in DNS (top-level domain then lower levels) order, and print to standard output.  With the --hosts flag, prepend each line with '127.0.0.1' and some whitespace for /etc/hosts blocking.  The purpose of this is to block ads and tracking sites.

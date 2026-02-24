#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# Clean up first before generating new files
DELETE_OUTPUT_DIRECTORY = True

# Disable relative URLs
RELATIVE_URLS = False

# Generate feeds
FEED_ATOM = "feeds/atom.xml"
FEED_RSS = "feeds/rss.xml"
FEED_ALL_ATOM = "feeds/all.atom.xml"
FEED_ALL_RSS = "feeds/all.rss.xml"

TEMPLATE_PAGES = {
    "sitemap.xml": "sitemap.xml",
    "llms-full.txt": "llms-full.txt",
}

GOATCOUNTER_ID = "sberrevoets"

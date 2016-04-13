#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# Enable relative URLs
RELATIVE_URLS = False

# Generate feeds
FEED_ATOM = 'feeds/atom.xml'
FEED_RSS = 'feeds/rss.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'

# Following items are often useful when publishing

DISQUS_SITENAME = 'sberrevoets'
#GOOGLE_ANALYTICS = ""

# Clean up
DELETE_OUTPUT_DIRECTORY = True

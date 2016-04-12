#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Site information
AUTHOR = 'Scott Berrevoets'
SITENAME = 'Scott Berrevoets'
SITEURL = 'http://scottberrevoets.com'

# Show line numbers in code snippets
MD_EXTENSIONS = ['codehilite(css_class=highlight, linenums = True)', 'extra']

# Path specifications
RELATIVE_URLS = False
PATH = 'content'
THEME = './theme'

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# Pagination
DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# Create and link to index and archive
DIRECT_TEMPLATES = ('index', 'archive')
MENUITEMS = [('Blog', '/'), ('Archive', '/archive.html')]

# Disable authors, categories, and tags
AUTHOR_SAVE_AS = False
CATEGORY_SAVE_AS = False
TAG_SAVE_AS = False

# Locale settings
DEFAULT_LANG = 'en'
TIMEZONE = 'America/Los_Angeles'
DATE_FORMATS = { 'en': '%d %B %Y' }

DISPLAY_SOCIAL_MEDIA = True
SOCIALMEDIAITEMS = [('twitter.svg', 'https://twitter.com/ScottBerrevoets'),
                    ('github.svg', 'https://github.com/sberrevoets'),
                    ('stackoverflow.svg', 'http://stackoverflow.com/users/751268/scott-berrevoets'),
                    ('youtube.svg', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Uncomment following line if you want document-relative URLs when developing

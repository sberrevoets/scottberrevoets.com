#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Site information
AUTHOR = "Scott Berrevoets"
SITENAME = "Scott Berrevoets"
SITEURL = "https://scottberrevoets.com"

# Show line numbers in code snippets
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
            "linenums": True,
        },
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {},
        "markdown.extensions.admonition": {},
    },
    "output_format": "html5",
}

# Path specifications
RELATIVE_URLS = True
PATH = "content"
THEME = "./theme"

ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"

PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

# Pagination
DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, "{base_name}/", "{base_name}/index.html"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)

# Create and link to index and archive
DIRECT_TEMPLATES = [("index")]
MENUITEMS = [("Blog", "")]

# Disable parsing HTML files
READERS = {"html": None}

# Disable authors, categories, and tags
AUTHOR_SAVE_AS = False
CATEGORY_SAVE_AS = False
TAG_SAVE_AS = False

# Locale settings
DEFAULT_LANG = "en"
TIMEZONE = "America/Los_Angeles"
DATE_FORMATS = {"en": "%B %d, %Y"}

# Social media
DISPLAY_SOCIAL_MEDIA = True
SOCIALMEDIAITEMS = [
    ("github.svg", "https://github.com/sberrevoets"),
    ("linkedin.svg", "https://linkedin.com/in/sberrevoets"),
    ("mastodon.svg", "https://hachyderm.io/@ScottBerrevoets"),
    ("mail.svg", "mailto:hi@scottberrevoets.com"),
]

# No feeds in development mode
FEED_DOMAIN = SITEURL

FEED_ATOM = None
FEED_RSS = None
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

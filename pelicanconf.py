#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Site information
AUTHOR = "Scott Berrevoets"
SITENAME = "Scott Berrevoets"
SITEURL = "https://scottberrevoets.com"
SITE_DESCRIPTION = "Scott Berrevoets is a software engineer working on long-lived software systems, especially around architecture, developer experience, and platform engineering."
FEATURED_POST_ORDER = [
    "review-your-own-ai-generated-code",
    "migration-strategies-in-large-codebases",
    "human-factors-in-choosing-technologies",
    "third-party-libraries-are-no-party-at-all",
    "shifting-the-testing-culture-motivation",
    "flywheel-of-tech-debt",
]
JINJA_GLOBALS = {"FEATURED_POST_ORDER": FEATURED_POST_ORDER}

# Don't show line numbers in code snippets by default
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
            "linenums": False,
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
STATIC_PATHS = ["images", "resume.pdf", "resume.html", "extra"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/llms.txt": {"path": "llms.txt"},
}

USE_FOLDER_AS_CATEGORY = True

ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"

PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

# Pages are linked manually in the menu
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
WITH_FUTURE_DATES = True

# Pagination
DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, "{base_name}/", "{base_name}/index.html"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)

# The homepage is generated from content/pages/home.md
DIRECT_TEMPLATES = []
MENUITEMS = [
    ("Home", ""),
    ("About", "about.html"),
    ("Blog", "blog.html"),
]

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
    ("github", "https://github.com/sberrevoets"),
    ("linkedin", "https://linkedin.com/in/sberrevoets"),
    ("mastodon", "https://hachyderm.io/@ScottBerrevoets"),
    ("mail", "mailto:hi@scottberrevoets.com"),
    ("rss", "/feeds/all.atom.xml"),
]

PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "readtime",
    "til_urls",
    "markdown_output",
]
READTIME_WPM = 200

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

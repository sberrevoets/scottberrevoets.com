#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Scott Berrevoets'
SITENAME = u'Scott Berrevoets'
SITEURL = ''

PATH = 'content'
THEME = './theme'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

DISPLAY_PAGES_ON_MENU = True
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

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

MD_EXTENSIONS = ['codehilite(css_class=highlight, linenums = True)', 'extra']
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

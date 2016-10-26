# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

import re


_star_bold = re.compile('\\*\\*([^*]+)\\*\\*')
_star_italic = re.compile('\\*([^*]+)\\*')
_underscore_bold = re.compile('__([^_]+)__')
_underscore_italic = re.compile('_([^_]+)_')
_monospace = re.compile('`([^`]+)`')


def safe_html(text):
    if not isinstance(text, basestring):
        raise ValueError('Not a string: %s' % text)

    # KEEP IN SYNC with javascript client side!

    text = text.replace('&', '&amp;') \
            .replace('<', '&lt;') \
            .replace('>', '&gt;')

    for pattern, replacement in (
            (_star_bold, '<strong>\\1</strong>'),
            (_star_italic, '<em>\\1</em>'),
            (_underscore_bold, '<strong>\\1</strong>'),
            (_underscore_italic, '<em>\\1</em>'),
            (_monospace, '<tt>\\1</tt>'),
            ):
        text = re.sub(pattern, replacement, text)

    return text

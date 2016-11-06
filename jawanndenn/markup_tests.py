# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from unittest import TestCase

from jawanndenn.markup import safe_html


class SafeHtmlTest(TestCase):
    def test_vanilla(self):
        self.assertEquals(safe_html(
                'text'),
                'text')

    def test_html(self):
        self.assertEquals(safe_html(
                '<b>&nbsp;</b>'),
                '&lt;b&gt;&amp;nbsp;&lt;/b&gt;')

    def test_bold(self):
        self.assertEquals(safe_html(
                '**text**'),
                '<strong>text</strong>')
        self.assertEquals(safe_html(
                '__text__'),
                '<strong>text</strong>')

    def test_italic(self):
        self.assertEquals(safe_html(
                '*text*'),
                '<em>text</em>')
        self.assertEquals(safe_html(
                '_text_'),
                '<em>text</em>')

    def test_monospace(self):
        self.assertEquals(safe_html(
                '`text`'),
                '<tt>text</tt>')

    def test_combined(self):
        self.assertEquals(safe_html(
                '`__*text*__`'),
                '<tt><strong><em>text</em></strong></tt>')
        self.assertEquals(safe_html(
                '`**_text_**`'),
                '<tt><strong><em>text</em></strong></tt>')
        self.assertEquals(safe_html(
                '_*text*_'),
                '<em><em>text</em></em>')

    def test_bad_nesting(self):
        self.assertEquals(safe_html(
                '*__text*__'),
                '<em><strong>text<em><strong></strong></em></strong></em>')

    def test_non_string(self):
        with self.assertRaises(ValueError):
            safe_html(123)

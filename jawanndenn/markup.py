# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

_REPLACEMENTS_IN_ORDER = (
    ("**", "<strong>", "</strong>"),
    ("*", "<em>", "</em>"),
    ("__", "<strong>", "</strong>"),
    ("_", "<em>", "</em>"),
    ("`", "<tt>", "</tt>"),
)

_CLOSING_OF = {prefix: closing for prefix, _, closing in _REPLACEMENTS_IN_ORDER}


def safe_html(text):
    if not isinstance(text, str):
        raise ValueError("Not a string: %s" % text)

    # KEEP IN SYNC with javascript client side!

    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    chunks = []

    opened = []
    while text:
        for prefix, opening, closing in _REPLACEMENTS_IN_ORDER:
            if text.startswith(prefix):
                if opened and opened[-1] == prefix:
                    # Close tag
                    chunks.append(closing)
                    opened.pop()
                else:
                    # Open tag
                    chunks.append(opening)
                    opened.append(prefix)

                text = text[len(prefix) :]
                break
        else:
            chunks.append(text[0])
            text = text[1:]

    # Close all unclosed tags
    for prefix in reversed(opened):
        chunks.append(_CLOSING_OF[prefix])

    return "".join(chunks)

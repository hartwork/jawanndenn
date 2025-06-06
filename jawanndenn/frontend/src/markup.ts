// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

const REPLACEMENTS_IN_ORDER = [
  ['**', '<strong>', '</strong>'],
  ['*', '<em>', '</em>'],
  ['__', '<strong>', '</strong>'],
  ['_', '<em>', '</em>'],
  ['`', '<tt>', '</tt>'],
];

const CLOSING_OF = {};
REPLACEMENTS_IN_ORDER.forEach((row) => {
  const prefix = row[0];
  const closing = row[2];
  CLOSING_OF[prefix] = closing;
});

// Excapes HTML and renders subset of markdown
const textToSafeHtml = (text: string): string => {
  // KEEP IN SYNC with python server side!
  text = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  const chunks = [];

  const opened = [];
  while (text.length) {
    let matched = false;

    REPLACEMENTS_IN_ORDER.forEach((row) => {
      const prefix = row[0];
      const opening = row[1];
      const closing = row[2];

      if (text.startsWith(prefix)) {
        if (opened.length && opened[opened.length - 1] == prefix) {
          // Close tag
          chunks.push(closing);
          opened.pop();
        } else {
          // Open tag
          chunks.push(opening);
          opened.push(prefix);
        }

        text = text.slice(prefix.length);

        matched = true;
        return false;
      }
    });

    if (!matched) {
      chunks.push(text[0]);
      text = text.slice(1);
    }
  }

  // Close all unclosed tags
  opened.reverse();
  opened.forEach((prefix) => {
    chunks.push(CLOSING_OF[prefix]);
  });

  return chunks.join('');
};

export { textToSafeHtml };

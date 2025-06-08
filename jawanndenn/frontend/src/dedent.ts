// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

const longestCommonPrefix = (s1: string, s2: string): string => {
  const minLength = Math.min(s1.length, s2.length);

  let i = 0;
  for (; i < minLength; i++) {
    if (s1[i] != s2[i]) {
      break;
    }
  }

  return s1.substring(0, i);
};

const indentOf = (line: string): string => {
  return line.substring(0, line.length - line.trimStart().length);
};

const dedent = (text: string): string => {
  const lines = text.split('\n');
  const longestSharedIndent = lines.reduce(
    (sharedIndent, line) =>
      longestCommonPrefix(indentOf(line) + sharedIndent, sharedIndent),
    indentOf(lines[0]),
  );
  return lines
    .map((line) => line.substring(longestSharedIndent.length))
    .join('\n');
};

export default dedent;

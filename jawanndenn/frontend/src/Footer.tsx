// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

import './Footer.css';

const Footer = () => {
  return (
    <footer>
      <p>
        <span style={{ fontSize: '150%', position: 'relative', top: '3px' }}>
          &#x2605;
        </span>
        <a href="https://github.com/hartwork/jawanndenn/">jawanndenn</a> is{' '}
        <a href="https://www.gnu.org/philosophy/free-sw.en.html">
          software libre
        </a>{' '}
        developed by <a href="https://blog.hartwork.org/">Sebastian Pipping</a>,
        licensed under the{' '}
        <a href="https://www.gnu.org/licenses/agpl.en.html">
          GNU Affero GPL license
        </a>
        . Please{' '}
        <a href="https://github.com/hartwork/jawanndenn/issues">report bugs</a>{' '}
        and let me know if you <a href="mailto:sebastian@pipping.org">like</a>{' '}
        it.
        <iframe
          id="github-star-button"
          src="./static/3rdparty/github-buttons-4.0.1/docs/github-btn.html?user=hartwork&amp;repo=jawanndenn&amp;type=star&amp;count=true"
          frameBorder="0"
          scrolling="0"
          width="170px"
          height="20px"
        ></iframe>
      </p>
    </footer>
  );
};

export default Footer;

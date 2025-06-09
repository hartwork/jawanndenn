// Copyright (c) 2025 Material UI authors
// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under MIT

import { createSvgIcon } from '@mui/material/utils';

// Source:
// https://github.com/mui/material-ui/blob/a4afa9ff2442589deb73a4b08c299913983967bd/packages/mui-material/src/internal/svg-icons/CheckBoxOutlineBlank.js
const CheckBoxOutlineBlankIcon = createSvgIcon(
  <path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z" />,
  'CheckBoxOutlineBlank',
);

// Source:
// https://github.com/mui/material-ui/blob/a4afa9ff2442589deb73a4b08c299913983967bd/packages/mui-material/src/internal/svg-icons/CheckBox.js
const CheckBoxIcon = createSvgIcon(
  <path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />,
  'CheckBox',
);

// Source:
// https://github.com/mui/material-ui/blob/a4afa9ff2442589deb73a4b08c299913983967bd/packages/mui-material/src/internal/svg-icons/IndeterminateCheckBox.js
const IndeterminateCheckBoxIcon = createSvgIcon(
  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10H7v-2h10v2z" />,
  'IndeterminateCheckBox',
);

export { CheckBoxOutlineBlankIcon, CheckBoxIcon, IndeterminateCheckBoxIcon };

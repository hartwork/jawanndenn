// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

import Checkbox from '@mui/material/Checkbox';
import {
  CheckBoxIcon,
  CheckBoxOutlineBlankIcon,
  IndeterminateCheckBoxIcon,
} from './CheckboxIcons.tsx';

const TristateCheckbox = ({
  name,
  tribool,
  setTribool,
}: {
  name: string;
  tribool: boolean | null;
  setTribool: (tribool: boolean | null) => void;
}) => {
  const checked = tribool === true;
  const indeterminate = tribool === null;
  const color = indeterminate ? 'maybe' : checked ? 'primary' : 'error';
  const value = indeterminate ? 'indeterminate' : checked ? 'on' : '';

  function onChange(_event) {
    if (indeterminate) {
      // indeterminate -> unchecked
      setTribool(false);
    } else if (checked) {
      // checked -> indeterminate
      setTribool(null);
    } else {
      // unchecked -> checked
      setTribool(true);
    }
  }

  return (
    <>
      <input name={name} type="hidden" value={value} />
      <Checkbox
        color={color}
        checked={checked}
        indeterminate={indeterminate}
        onChange={onChange}
        icon={<CheckBoxOutlineBlankIcon />}
        checkedIcon={<CheckBoxIcon />}
        indeterminateIcon={<IndeterminateCheckBoxIcon />}
      />
    </>
  );
};

export default TristateCheckbox;

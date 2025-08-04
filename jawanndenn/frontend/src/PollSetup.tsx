// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

import './PollSetup.css';
import dedent from './dedent.ts';

import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import TextField from '@mui/material/TextField';

import { parse as parseYaml } from 'yaml';

const DEFAULT_CONFIG_YAML = dedent(`\
  title: Which fruit do _**you**_ like?

  options:
    - Apple
    - Banana
    - Orange
    - Papaya

  lifetime: month
`);

class InvalidConfigError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'InvalidConfigError';
    // NOTE: This will make "e instanceof InvalidConfigError" work
    Object.setPrototypeOf(this, InvalidConfigError.prototype);
  }
}

const parseConfigText = (text: string) => {
  const parsed = parseYaml(text); // may throw

  // .lifetime
  if (!['month', 'week', undefined].includes(parsed.lifetime)) {
    throw new InvalidConfigError(
      "Attribute 'lifetime' is invalid, must be 'month' or 'week'.",
    );
  }

  // .options
  if (parsed.options === undefined) {
    throw new InvalidConfigError("Attribute 'options' is missing.");
  }

  if (!Array.isArray(parsed.options)) {
    throw new InvalidConfigError("Attribute 'options' is not a list.");
  }

  if (!parsed.options.every((v) => typeof v === 'string')) {
    throw new InvalidConfigError(
      "Attribute 'options' is not a list of strings.",
    );
  }

  // .title
  if (parsed.title === undefined) {
    throw new InvalidConfigError("Attribute 'title' is missing.");
  }
  if (typeof parsed.title !== 'string') {
    throw new InvalidConfigError("Attribute 'title' is not a string.");
  }

  return parsed;
};

const DEFAULT_CONFIG = parseConfigText(DEFAULT_CONFIG_YAML);

const DEFAULT_CONFIG_STATE = [DEFAULT_CONFIG_YAML, true, DEFAULT_CONFIG];

type ConfigTripel = [string, boolean, PollConfig];
type ConfigTripelSetter = (_: ConfigTripel) => void;

const PollSetup = ({
  configState,
}: {
  configState: [ConfigTripel, ConfigTripelSetter];
}) => {
  const [[configText, isValid, latestValidConfig], setConfig] = configState;

  const onChange = (e) => {
    const newConfigText = e.target.value;
    let newIsValid = false;
    let newParsed = null;
    try {
      newParsed = parseConfigText(newConfigText);
      newIsValid = true;
    } catch (error) {
      console.log(
        '[DEBUG]',
        'Config YAML/JSON failed to validate with error:',
        error.message,
      );
      newParsed = latestValidConfig;
    }
    setConfig([newConfigText, newIsValid, newParsed]);
  };

  const onReset = (_event) => {
    setConfig(DEFAULT_CONFIG_STATE);
  };

  return (
    <div className="setup">
      <form action="create" method="POST">
        <Card>
          <input
            type="hidden"
            name="csrfmiddlewaretoken"
            value={window.DJANGO_CSRF_TOKEN}
          />
          <CardContent>
            <TextField
              name="config"
              label="Setup (YAML or JSON)"
              multiline
              value={configText}
              variant="standard"
              onChange={onChange}
              className={`monospace-text ${isValid ? 'valid' : 'invalid'}`}
              autoFocus
              error={!isValid}
            />
          </CardContent>
          <CardActions
            className="setupButtons"
            sx={{
              justifyContent: 'flex-end',
            }}
          >
            <Button variant="text" onClick={onReset} color="inherit">
              RESET
            </Button>
            <Button type="submit" variant="contained" disabled={!isValid}>
              CREATE
            </Button>
          </CardActions>
        </Card>
      </form>
    </div>
  );
};

export { DEFAULT_CONFIG_STATE, PollSetup };

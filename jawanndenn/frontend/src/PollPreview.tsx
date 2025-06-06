// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

import { Poll, PollConfig } from './Poll.tsx';

const EXAMPLE_PEOPLE = ['Dmitri', 'Jule', 'Vered', 'Matthieu'];

const randomVoteCache = {};

const getCachedRandomVote = (person, option) => {
  const key = `${person}@${option}`;
  let value: bool | undefined = randomVoteCache[key];
  if (value === undefined) {
    value = Math.random() > 0.5;
    randomVoteCache[key] = value;
  }
  return value;
};

const PollPreview = ({ config }: { config: PollConfig }) => {
  const votes = EXAMPLE_PEOPLE.map((person, personIndex) => [
    person,
    config.options.map((_option, optionIndex) =>
      getCachedRandomVote(personIndex, optionIndex),
    ),
  ]);

  return <Poll config={config} votes={votes} pretend={true} />;
};

export default PollPreview;

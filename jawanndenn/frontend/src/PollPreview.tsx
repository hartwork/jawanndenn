// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

import { Poll, PollConfig } from './Poll.tsx';

const EXAMPLE_PEOPLE = ['Dmitri', 'Jule', 'Vered', 'Matthieu'];

const randomVoteCache = {};
let randomVotesAny = 0;
let randomVotesNull = 0;

const getCachedRandomVote = (person, option) => {
  const key = `${person}@${option}`;
  let value: bool | undefined = randomVoteCache[key];
  if (value === undefined) {
    const commonCoiceCount = 4;
    const forceOneMaybeAfter = (EXAMPLE_PEOPLE.length * commonCoiceCount) / 2;
    if (randomVotesAny > forceOneMaybeAfter && randomVotesNull == 0) {
      value = null;
    } else {
      const zeroToOne = Math.random();
      value = zeroToOne > 0.95 ? null : zeroToOne > 0.95 / 2 ? true : false;
    }

    randomVotesAny += 1;
    if (value === null) {
      randomVotesNull += 1;
    }

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

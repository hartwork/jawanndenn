// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

import './Poll.css';
import { textToSafeHtml } from './markup.ts';
import TristateCheckbox from './TristateCheckbox.tsx';

import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import TextField from '@mui/material/TextField';

import { useState } from 'react';

const HEAVY_CHECK_MARK = '\u2714';
const HEAVY_BALLOT_X = '\u2718';

// TODO
type PollConfig = {}; // eslint-disable-line @typescript-eslint/no-empty-object-type
type PollVotes = {}; // eslint-disable-line @typescript-eslint/no-empty-object-type

const Poll = ({
  pollId,
  config,
  votes,
  titleIsHtml = false,
  pretend = false,
}: {
  pollId: string | undefined;
  config: PollConfig;
  votes: PollVotes;
  titleIsHtml: boolean;
  pretend: boolean;
}) => {
  const [originalUsersVotes, setUsersVotes] = useState([]);
  const [usersName, setUsersName] = useState('');

  // Auto-correct user's votes to always have the same length as config.options
  let usersVotes = originalUsersVotes;
  if (originalUsersVotes.length > config.options.length) {
    usersVotes = originalUsersVotes.slice(0, config.options.length);
  } else if (originalUsersVotes.length < config.options.length) {
    const filling = config.options
      .slice(originalUsersVotes.length)
      .map((_) => false);
    usersVotes = originalUsersVotes.concat(filling);
  }
  console.assert(usersVotes.length === config.options.length);

  const yesSummary = config.options.map((_option, index) =>
    votes.reduce(
      (sum, [_person, person_votes]) => sum + (person_votes[index] ? 1 : 0),
      usersVotes[index] ? 1 : 0,
    ),
  );
  const notNoSummary = config.options.map((_option, index) =>
    votes.reduce(
      (sum, [_person, person_votes]) =>
        sum + (person_votes[index] !== false ? 1 : 0),
      [true, null].includes(usersVotes[index]) ? 1 : 0,
    ),
  );
  const combinedSummary = config.options.map((_option, index) =>
    notNoSummary[index] > yesSummary[index]
      ? `${yesSummary[index]}–${notNoSummary[index]}`
      : yesSummary[index],
  );

  const createSetTribool = (column) => {
    const setTribool = (yes) => {
      const newUsersVotes = usersVotes.slice();
      newUsersVotes[column] = yes;
      setUsersVotes(newUsersVotes);
    };
    return setTribool;
  };

  return (
    <Card className={`poll ${pretend ? 'preview' : ''}`}>
      {pretend && <CardHeader title="Preview" />}
      <CardContent>
        <h2
          dangerouslySetInnerHTML={{
            __html: titleIsHtml ? config.title : textToSafeHtml(config.title),
          }}
          className="question"
        />

        <form method="POST" action={`vote/${pollId}`}>
          <input
            type="hidden"
            name="csrfmiddlewaretoken"
            value={window.DJANGO_CSRF_TOKEN}
          />
          <table>
            {/* Header */}
            <thead>
              <tr>
                <td />
                {config.options.map((e, index) => (
                  <td key={index} className="vote">
                    {e}
                  </td>
                ))}
                <td />
              </tr>
            </thead>

            <tbody>
              {
                /* Other users' votes */
                votes.map(([person, persons_votes], row) => (
                  <tr key={row}>
                    <td
                      dangerouslySetInnerHTML={{ __html: person }}
                      className="person"
                    />
                    {persons_votes.map((yes, column) => (
                      <td
                        key={column}
                        className={`vote ${yes ? 'votedYes' : yes === null ? 'votedMaybe' : 'votedNo'}`}
                      >
                        {yes ? (
                          HEAVY_CHECK_MARK
                        ) : yes === null ? (
                          <b>?</b>
                        ) : (
                          HEAVY_BALLOT_X
                        )}
                      </td>
                    ))}
                    <td />
                  </tr>
                ))
              }

              {/* User vote */}
              <tr className="userVote">
                <td>
                  <TextField
                    name="voterName"
                    placeholder="Your name"
                    variant="standard"
                    autoFocus={!pretend}
                    value={usersName}
                    onChange={(e) => setUsersName(e.target.value)}
                    error={!pretend && !usersName.trim()}
                    className="voterName"
                  />
                </td>
                {usersVotes.map((yes, column) => (
                  <td
                    key={column}
                    className={`vote ${
                      yes ? 'votedYes' : yes === null ? 'votedMaybe' : 'votedNo'
                    }`}
                  >
                    <TristateCheckbox
                      name={`option${column}`}
                      tribool={yes}
                      setTribool={createSetTribool(column)}
                    />
                  </td>
                ))}
                <td>
                  {' '}
                  <Button
                    variant="contained"
                    disabled={pretend || !usersName.trim()}
                    type="submit"
                    className="submitVote"
                  >
                    SAVE
                  </Button>
                </td>
              </tr>

              {/* Summary */}
              <tr>
                <td />
                {combinedSummary.map((sum, column) => (
                  <td
                    key={column}
                    className={`vote ${sum ? 'sumNonZero' : ''}`}
                  >
                    {sum}
                  </td>
                ))}
                <td />
              </tr>
            </tbody>
          </table>
        </form>
      </CardContent>
    </Card>
  );
};

export { Poll, PollConfig };

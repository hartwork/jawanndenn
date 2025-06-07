// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU Affero GPL v3 or later

import './Poll.css';
import { textToSafeHtml } from './markup.ts';

import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Checkbox from '@mui/material/Checkbox';
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
      .map((_) => null);
    usersVotes = originalUsersVotes.concat(filling);
  }
  console.assert(usersVotes.length === config.options.length);

  const summary = config.options.map((_option, index) =>
    votes.reduce(
      (sum, [_person, person_votes]) => sum + (person_votes[index] ? 1 : 0),
      usersVotes[index] ? 1 : 0,
    ),
  );

  const onCheckboxChange = (column) => {
    const onChange = (e) => {
      const newUsersVotes = usersVotes.slice();
      newUsersVotes[column] = e.target.checked;
      setUsersVotes(newUsersVotes);
    };
    return onChange;
  };

  return (
    <Card className="poll">
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
                        className={`vote ${yes ? 'votedYes' : 'votedNo'}`}
                      >
                        {yes ? HEAVY_CHECK_MARK : HEAVY_BALLOT_X}
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
                      yes ? 'votedYes' : yes === null ? 'yetToVote' : 'votedNo'
                    }`}
                  >
                    <Checkbox
                      name={`option${column}`}
                      checked={yes}
                      onChange={onCheckboxChange(column)}
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
                {summary.map((sum, column) => (
                  <td
                    key={column}
                    className={`vote ${sum > 0 ? 'sumNonZero' : ''}`}
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

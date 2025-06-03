// Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
// Licensed under GNU GPL v3 or later

import './App.css';

import Footer from './Footer.tsx';
import { Poll } from './Poll.tsx';
import PollPreview from './PollPreview.tsx';
import { DEFAULT_CONFIG_STATE, PollSetup } from './PollSetup.tsx';

import { useState } from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Grid from '@mui/material/Grid';

const fetchPollData = async (pollId, setResponse) => {
  const url = `data/${pollId}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(
        `HTTP request to '${url}' failed with status ${response.status}.`,
      );
    }
    const parsed = await response.json();
    setResponse(parsed);
  } catch (error) {
    console.error('ERROR:', error.message);
  }
};

const pollId = window.location.pathname.includes('/poll/')
  ? /[0-9a-fA-F]{64}/.exec(window.location.pathname)[0]
  : null;

if (pollId) {
  document.title = 'jawanndenn: Vote!';
}

const theme = createTheme({
  palette: {
    primary: {
      main: '#26a69a',
    },
  },
});

const SinglePollApp = ({ pollId }: { pollId: string }) => {
  const [response, setResponse] = useState(null);

  if (response) {
    return (
      <Grid
        container
        spacing={2}
        sx={{
          justifyContent: 'safe center',
          alignItems: 'flow-start',
        }}
      >
        <Grid size={{ xs: 12, sm: 12, md: 'auto', lg: 'auto', xl: 'auto' }}>
          <div className="live">
            <Poll
              pollId={pollId}
              config={response.config}
              votes={response.votes}
              titleIsHtml={true}
            />
          </div>
        </Grid>
      </Grid>
    );
  }

  fetchPollData(pollId, setResponse); // not blocking because async

  return <></>;
};

const SetupAndPreviewApp = () => {
  const configState = useState(DEFAULT_CONFIG_STATE);
  const config = configState[0][2];

  return (
    <Grid
      container
      spacing={2}
      sx={{
        justifyContent: 'safe center',
      }}
    >
      <Grid size={{ xs: 12, sm: 12, md: 4, lg: 3, xl: 3 }}>
        <PollSetup configState={configState} />
      </Grid>
      <Grid size={{ xs: 12, sm: 12, md: 'auto', lg: 'auto', xl: 'auto' }}>
        <PollPreview config={config} />
      </Grid>
    </Grid>
  );
};

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <div className="stage">
        {pollId ? <SinglePollApp pollId={pollId} /> : <SetupAndPreviewApp />}
      </div>
      <Footer />
    </ThemeProvider>
  );
};

export default App;

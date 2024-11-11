'use client';

import { Button, Column, Grid, SkeletonText, ToastNotification } from '@carbon/react';

import React, { useEffect, useState } from 'react';
import { Octokit } from '@octokit/core';
import PromptMap from './PromptMap';
import { Add, TextStrikethrough } from '@carbon/react/icons';
import Prompt from './Prompt';
import { context } from '../providers';
import { getEnv } from '../env';

const octokitClient = new Octokit({});

function PromptsPage() {
  let env = context()?.env;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();
  const [rows, setRows] = useState([]);

  const [open, setOpen] = useState(false);

  useEffect(() => {
    try {
      if (!env.backendBaseAPI) {
        env = getEnv();
      }
      getPrompts();
    } finally {
      setLoading(false);
    }
  }, []);

  const getPrompts = async () => {
    try {
      const res = await octokitClient.request(
        `GET ${env.backendBaseAPI}a/prompts/`);

      if (res.status === 200) {
        setRows(res.data);
      } else {
        setError('Error obtaining prompt data (' + res.status + ')');
      }
    } catch (error) {
      setError('Error obtaining prompt data:' + error.message);
      console.error('Error obtaining prompt data:', error);
    } finally {
      setLoading(false);
    }
  }

  const reloadPrompts = () => {
    setLoading(true);
    getPrompts();
  }

  return (
    <Grid>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <h1 className="landing-page__heading">Prompts</h1>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <Button renderIcon={Add} iconDescription="Add Prompt" onClick={() => setOpen(true)}>Add Prompt</Button>
        <Prompt backendBaseAPI={env.backendBaseAPI} mode="create" prompt={null} prompts={rows} openState={open} setOpenState={setOpen} onSuccess={reloadPrompts} setError={setError} />
      </Column>

      {loading && (
        <Column lg={3} md={2} sm={2}>
          <SkeletonText className="card" paragraph={true} lineCount={2} />
        </Column>
      )}

      {!loading && (<PromptMap backendBaseAPI={env.backendBaseAPI} rows={rows} setRows={setRows} setError={setError} reloadPrompts={reloadPrompts} />)}

      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        {error && (<ToastNotification role="alert" caption={error} timeout={3000} title="Error" subtitle="" />)}
      </Column>
    </Grid>
  );
}

export default PromptsPage;

'use client';

import { Button, Column, Grid, SkeletonText, ToastNotification } from '@carbon/react';

import React, { useEffect, useState } from 'react';
import { Octokit } from '@octokit/core';
import ToolMap from './ToolMap';
import { Add } from '@carbon/react/icons';
import Tool from './Tool';
import { useEnv } from '../providers';
import { getEnv } from '../env';

const octokitClient = new Octokit({});

function ToolsPage() {
  let env = useEnv();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();
  const [rows, setRows] = useState([]);

  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!env.backendBaseAPI) {
      getEnv().then((e) => {
        env = e;
        getTools();
      })
    } else {
      getTools();
    }
  }, []);

  const getTools = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/tools`);
      if (res.status === 200) {
        setRows(res.data);
      } else {
        setError('Error obtaining tool data (' + res.status + ')');
      }
    } catch (error) {
      setError('Error obtaining tool data:' + error.message);
      console.error('Error obtaining tool data:' + error.message);
    }
    setLoading(false);
  }

  const reloadTools = () => {
    setLoading(true);
    getTools();
  }

  return (
    <Grid>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <h1 className="landing-page__heading">Tools</h1>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <Button renderIcon={Add} iconDescription="Add Tool" onClick={() => setOpen(true)}>Add Tool</Button>
        <Tool mode="create" tool={null} tools={rows} openState={open} setOpenState={setOpen} onSuccess={reloadTools} setError={setError} />
      </Column>

      {loading && (
        <Column lg={3} md={2} sm={2}>
          <SkeletonText className="card" paragraph={true} lineCount={2} />
        </Column>
      )}

      {!loading && (<ToolMap rows={rows} setRows={setRows} setError={setError} reloadTools={reloadTools} />)}

      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        {error && (<ToastNotification role="alert" caption={error} timeout={3000} title="Error" subtitle="" />)}
      </Column>
    </Grid>
  );
}

export default ToolsPage;

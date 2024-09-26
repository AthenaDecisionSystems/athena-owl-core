'use client';

import { Breadcrumb, BreadcrumbItem, Button, Column, Grid, SkeletonText, ToastNotification } from '@carbon/react';

import React, { useEffect, useState } from 'react';
import { Octokit } from '@octokit/core';
import AssistantMap from './AssistantMap';
import { Add } from '@carbon/react/icons';
import Assistant from './Assistant';
import { context } from "../providers";
import { getEnv } from '../env';

const octokitClient = new Octokit({});

function AssistantsPage() {
  let env = context()?.env;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();
  const [rows, setRows] = useState([]);

  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!env.backendBaseAPI) {
      getEnv().then((e) => {
        env = e;
        getAssistants();
      })
    } else {
      getAssistants();
    }
  }, []);

  const getAssistants = async () => {
    try {
      const res = await octokitClient.request(
        `GET ${env.backendBaseAPI}a/assistants`,
        {
          //per_page: 75,
          //sort: 'updated',
          //direction: 'desc',
        }
      );

      if (res.status === 200) {
        setRows(res.data);
      } else {
        setError('Error obtaining assistant data (' + res.status + ')');
      }
    } catch (error) {
      setError('Error obtaining assistant data:' + error.message);
      console.error('Error obtaining assistant data:' + error.message);
    }
    setLoading(false);
  }

  const reloadAssistants = () => {
    setLoading(true);
    getAssistants();
  }

  return (
    <Grid>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <Breadcrumb noTrailingSlash aria-label="Page navigation">
          <BreadcrumbItem>
            <a href="/">Manage intelligent decision with Hybrid AI</a>
          </BreadcrumbItem>
        </Breadcrumb>
        <h1 className="landing-page__heading">Assistants</h1>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <Button renderIcon={Add} iconDescription="Add Assistant" onClick={() => setOpen(true)}>Add Assistant</Button>
        <Assistant mode="create" assistants={rows} openState={open} setOpenState={setOpen} onSuccess={reloadAssistants} setError={setError} />
      </Column>

      {loading && (
        <Column lg={3} md={2} sm={2}>
          <SkeletonText className="card" paragraph={true} lineCount={2} />
        </Column>
      )}

      {!loading && (<AssistantMap rows={rows} setRows={setRows} setError={setError} reloadAssistants={reloadAssistants} />)}

      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        {error && (<ToastNotification role="alert" caption={error} timeout={5000} title="Error" subtitle="" />)}
      </Column>
    </Grid>
  );
}

export default AssistantsPage;

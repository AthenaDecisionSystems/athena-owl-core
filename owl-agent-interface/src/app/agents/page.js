'use client';

import { Button, Column, Grid, SkeletonText, ToastNotification, Toggle } from '@carbon/react';

import React, { useEffect, useState } from 'react';
import { Octokit } from '@octokit/core';
import AgentMap from './AgentMap';
import { Add } from '@carbon/react/icons';
import Agent from './Agent';
import { context } from '../providers';
import { getEnv } from '../env';
import { useTranslation } from 'react-i18next';

const octokitClient = new Octokit({});

function AgentsPage() {
  let env = context()?.env;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();
  const [rows, setRows] = useState([]);
  const [prompts, setPrompts] = useState([]);
  const [runnerClassNames, setRunnerClassNames] = useState([]);

  const [open, setOpen] = useState(false);
  const [showHiddenAgents, setShowHiddenAgents] = useState(false);

  const { t, i18n } = useTranslation();

  useEffect(() => {
    try {
      if (!env.backendBaseAPI) {
        env = getEnv();
      }
      getAgents();
      getPrompts();
    } finally {
      setLoading(false);
    }
  }, []);

  const getAgents = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/agents/`);
      if (res.status === 200) {
        setRows(res.data);

        // Get Runner class names list
        const listFromAgents = res.data.map(agent => agent.runner_class_name);
        const uniqueValues = new Set();
        const deduplicated = listFromAgents.filter(item => {
          if (!uniqueValues.has(item)) {
            uniqueValues.add(item);
            return true;
          }
          return false;
        });
        setRunnerClassNames(deduplicated.map(item => ({ name: (item === "athena.llm.agents.agent_mgr.OwlAgentDefaultRunner" ? "Owl Agent Default Runner" : item), value: item })));
      } else {
        setError('Error obtaining agent data (' + res.status + ')');
      }
    } catch (error) {
      setError('Error obtaining agent data:' + error.message);
      console.error('Error obtaining agent data:', error);
    }
  }

  const getPrompts = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/prompts/`);
      if (res.status === 200) {
        setPrompts(res.data);
      } else {
        setError('Error obtaining prompt data (' + res.status + ')');
        console.error('Error obtaining prompt data ', res);
      }
    } catch (error) {
      setError('Error obtaining prompt data:' + error.message);
      console.error('Error obtaining prompt data:' + error);
    }
  }

  const reloadAgents = () => {
    setLoading(true);
    try {
      getAgents();
      getPrompts();
    } finally {
      setLoading(false);
    }
  }

  return (
    <Grid>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <h1 className="landing-page__heading">Agents</h1>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <Button renderIcon={Add} iconDescription="Add Agent" onClick={() => setOpen(true)}>Add Agent</Button>
        {!loading && (<Agent backendBaseAPI={env.backendBaseAPI} mode="create" agents={rows} agent={null} prompts={prompts} runnerClassNames={runnerClassNames} openState={open} setOpenState={setOpen} onSuccess={reloadAgents} setError={setError} />)}
      </Column>
      {loading && (
        <Column lg={3} md={2} sm={2}>
          <SkeletonText className="card" paragraph={true} lineCount={2} />
        </Column>
      )}

      {!loading && (<AgentMap backendBaseAPI={env.backendBaseAPI} rows={rows} setRows={setRows} prompts={prompts} runnerClassNames={runnerClassNames} showHiddenAgents={showHiddenAgents} setError={setError} reloadAgents={reloadAgents} />)}

      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <Toggle id="show-hidden-agents"
          size="sm"
          labelText="Show hidden agents"
          defaultToggled={showHiddenAgents}
          labelA="No"
          labelB="Yes"
          onClick={() => setShowHiddenAgents(!showHiddenAgents)} />
        <br />
        {error && (<ToastNotification role="alert" caption={error} timeout={5000} title="Error" subtitle="" />)}
      </Column>
    </Grid>
  );
}

export default AgentsPage;

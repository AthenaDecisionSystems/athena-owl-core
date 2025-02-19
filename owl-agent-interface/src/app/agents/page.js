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
  const [modelClassNames, setModelClassNames] = useState([]);

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
      loadModelClassNames();
    } finally {
      setLoading(false);
    }
  }, []);

  const getAgents = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/agents`);
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
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/prompts`);
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

  const loadModelClassNames = async () => {
    // setModelClassNames([
    //   { name: "Anthropic", value: "langchain_anthropic.ChatAnthropic", modelNames: ["claude-3-opus-20240229"] },
    //   { name: "Mistral AI", value: "langchain_mistralai.chat_models.ChatMistralAI", modelNames: ["mistral-large-latest", "open-mixtral-8x7b",] },
    //   { name: "Open AI", value: "langchain_openai.ChatOpenAI", modelNames: ["gpt-4o-2024-08-06", "gpt-4-turbo", "gpt-3.5-turbo"] },
    //   { name: "Watsonx LLM", value: "langchain_ibm.WatsonxLLM", modelNames: ['google/flan-t5-xl', 'google/flan-t5-xxl', 'google/flan-ul2', 'ibm/granite-13b-chat-v2', 'ibm/granite-13b-instruct-v2', 'ibm/granite-20b-multilingual', 'ibm/granite-7b-lab', 'meta-llama/llama-2-13b-chat', 'meta-llama/llama-3-1-70b-instruct', 'meta-llama/llama-3-1-8b-instruct', 'meta-llama/llama-3-70b-instruct', 'meta-llama/llama-3-8b-instruct', 'mistralai/mistral-large', 'mistralai/mixtral-8x7b-instruct-v01'] },
    //   { name: "Chat Watsonx", value: "langchain_ibm.ChatWatsonx", modelNames: ['mistralai/mistral-large'] },
    // ]);
    try {
      const res = await fetch(`${env.backendBaseAPI}a/agents/providers`);
      if (res.ok) {
        const data = await res.json();
        setModelClassNames(data);
      } else {
        setError('Error obtaining model class names (' + res.status + ')');
      }
    } catch (error) {
      setError('Error obtaining model class names:' + error.message);
      console.error('Error obtaining model class names:', error);
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
        {!loading && (<Agent backendBaseAPI={env.backendBaseAPI} mode="create" agents={rows} agent={null} prompts={prompts} runnerClassNames={runnerClassNames} modelClassNames={modelClassNames} openState={open} setOpenState={setOpen} onSuccess={reloadAgents} setError={setError} />)}
      </Column>
      {loading && (
        <Column lg={3} md={2} sm={2}>
          <SkeletonText className="card" paragraph={true} lineCount={2} />
        </Column>
      )}

      {!loading && (<AgentMap backendBaseAPI={env.backendBaseAPI} rows={rows} setRows={setRows} prompts={prompts} runnerClassNames={runnerClassNames} modelClassNames={modelClassNames} showHiddenAgents={showHiddenAgents} setError={setError} reloadAgents={reloadAgents} />)}

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

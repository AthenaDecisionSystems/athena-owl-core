'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Accordion, AccordionItem, Button, Column, Dropdown, DropdownSkeleton, Grid, Select, SelectItem, Stack, ToastNotification, Toggle } from '@carbon/react';
import { Reset, Trusted } from '@carbon/pictograms-react';
import { Octokit } from '@octokit/core';
import { context } from '../providers';
import { getEnv } from '../env';
import { useTranslation } from 'react-i18next';
import OwlAgent from '../agents/OwlAgent';

const octokitClient = new Octokit({});

function AgentsPage() {
  let env = context()?.env;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();
  const [agents, setAgents] = useState([]);
  const [useFileSearch, setUseFileSearch] = useState(true);
  const [useDecisionServices, setUseDecisionServices] = useState(false);
  const [activeAgent, setActiveAgent] = useState(null);
  const [randomNumber, setRandomNumber] = useState(0);
  const [agentModelName, setAgentModelName] = useState("");
  const [agentModelClassName, setAgentModelClassName] = useState("");
  const [showSettings, setShowSettings] = useState(true);
  const [showDocuments, setShowDocuments] = useState(false);

  const { t, i18n } = useTranslation();

  const modelClassNames = [
    { name: "Anthropic", value: "langchain_anthropic.ChatAnthropic", modelNames: ["claude-3-opus-20240229"] },
    { name: "Mistral AI", value: "langchain_mistralai.chat_models.ChatMistralAI", modelNames: ["mistral-large-latest", "open-mixtral-8x7b",] },
    { name: "Open AI", value: "langchain_openai.ChatOpenAI", modelNames: ["gpt-4o-2024-08-06", "gpt-4-turbo", "gpt-3.5-turbo"] },
    { name: "Watsonx LLM", value: "langchain_ibm.WatsonxLLM", modelNames: ['google/flan-t5-xl', 'google/flan-t5-xxl', 'google/flan-ul2', 'ibm/granite-13b-chat-v2', 'ibm/granite-13b-instruct-v2', 'ibm/granite-20b-multilingual', 'ibm/granite-7b-lab', 'meta-llama/llama-2-13b-chat', 'meta-llama/llama-3-1-70b-instruct', 'meta-llama/llama-3-1-8b-instruct', 'meta-llama/llama-3-70b-instruct', 'meta-llama/llama-3-8b-instruct', 'mistralai/mistral-large', 'mistralai/mixtral-8x7b-instruct-v01'] },
    { name: "Chat Watsonx", value: "langchain_ibm.ChatWatsonx", modelNames: ['mistralai/mistral-large'] },
  ];

  const owlAgentRef = useRef();

  useEffect(() => {
    // Disable scrolling
    document.body.style.overflow = 'hidden';
    return () => {
      // Re-enable scrolling when disassembling a component
      document.body.style.overflow = 'auto';
    };
  }, []);

  useEffect(() => {
    const loadData = async () => {
      const agents = await getAgents();
      setAgents(agents);
      if (agents?.length > 0) {
        setActiveAgent(agents[0]);
      }
    }

    try {
      if (!env?.backendBaseAPI) {
        env = getEnv();
      }
      loadData();
    } finally {
      setLoading(false);
    }
    setRandomNumber(Math.floor(Math.random() * 1000000000));
  }, []);

  useEffect(() => {
    if (activeAgent) {
      setAgentModelName(activeAgent.modelName);
      setAgentModelClassName(activeAgent.modelClassName);
      if (activeAgent.modelName && activeAgent.modelClassName) {
        const llm = modelClassNames.find((modelClassName) => (modelClassName.value === activeAgent.modelClassName)).name;
        owlAgentRef.current.informUser(`Agent **${activeAgent.name}** is set to use the LLM **${llm}** with the model **${activeAgent.modelName}**`);
      }
    }
  }, [activeAgent]);

  const getAgents = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/agents`);
      if (res.status === 200) {
        return res.data;
      } else {
        setError('Error obtaining agent data (' + res.status + ')');
      }
    } catch (error) {
      setError('Error obtaining agent data:' + error.message);
      console.error('Error obtaining agent data:', error);
    }
  }

  const updateAgent = async () => {
    // If this is is the first time the agent is being updated, we need to create a temporary agent object with the same name and properties as the active agent
    // We will then use this object to update the agent with the new values
    // If the agent has already been updated once, we will use the agent object that was created the first time
    let agentToUpdate = activeAgent;
    let firstTimeUpdate = false;
    let agentId = activeAgent.agent_id;
    let action = "PUT ";
    if (!activeAgent.updated) {
      firstTimeUpdate = true;
      action = "POST ";
      agentId += "_" + Date.now() + "_temp";
      agentToUpdate = { ...activeAgent, updated: true, originalAgentId: activeAgent.agent_id, agent_id: agentId };
    }

    // Update the agent with the new values
    agentToUpdate.modelName = agentModelName;
    agentToUpdate.modelClassName = agentModelClassName;

    // Update the agent in the backend
    try {
      const res = await octokitClient.request(
        action + env.backendBaseAPI + "a/agents/" + (firstTimeUpdate ? "" : agentId), {
        agent_id: agentId,
        name: agentToUpdate.name + "*",
        description: agentToUpdate.description,
        modelName: agentModelName,
        modelClassName: agentModelClassName,
        runner_class_name: agentToUpdate.runner_class_name,
        prompt_ref: agentToUpdate.prompt_ref,
        temperature: agentToUpdate.temperature,
        top_k: agentToUpdate.top_k,
        top_p: agentToUpdate.top_p,
        tools: agentToUpdate.tools,
        hidden_to_ui: true
      });

      if (res.status === 200) {
        // Replace the active agent with the updated agent in the agents list
        const newAgents = agents.map(agent => agent.agent_id === agentToUpdate.originalAgentId ? agentToUpdate : agent);
        setAgents(newAgents);
        setActiveAgent(agentToUpdate);
        owlAgentRef.current.updateAgent();

        console.log('Agent updated successfully');
      } else {
        setError('Error updating agent (' + res.status + ')');
        console.error('Error updating agent ', res);
      }
    } catch (error) {
      setError('Error updating agent:' + error.message);
      console.error('Error updating agent:', error);
    }
  }

  const changeModelName = (e) => {
    setAgentModelName(e.target.value);
    updateAgent();
  }

  const changeModelClassName = (e) => {
    setAgentModelClassName(e.target.value);
    setAgentModelName(modelClassNames.find((modelClassName) => (modelClassName.value === e.target.value)).modelNames[0]);
    updateAgent();
  }

  const toggleUseDecisionServices = () => {
    setUseDecisionServices(!useDecisionServices);
    owlAgentRef.current.resetConversation()
  }

  const toggleUseFileSearch = () => {
    setUseFileSearch(!useFileSearch);
    owlAgentRef.current.resetConversation()
  }

  const onChangeAgent = (e) => {
    setActiveAgent(e.selectedItem);
    owlAgentRef.current.resetConversation()
  }

  return (
    <Grid condensed>
      <Column lg={4} md={2} sm={1} className="page__r4">
        {loading || !activeAgent && (<DropdownSkeleton />)}
        {!loading && activeAgent && <Dropdown id={"agentId"}
          titleText={"Agent"}
          items={agents}
          itemToString={(item) => (item ? item.name ? item.name : item.agent_id : "")}
          selectedItem={activeAgent}
          onChange={(e) => onChangeAgent(e)}
          disabled={false} />}
        <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem', height: '1rem' }} />

        <Accordion>
          <AccordionItem key="1" title="Settings" className="owl-agent-config-accordion-item" open={showSettings} onClick={() => { setShowSettings(Trusted); setShowDocuments(false) }}>
            <Stack gap={4} style={{ width: "100%" }}>
              <Toggle id={"UseFileSearch"}
                labelText={"Use File Search"}
                toggled={useFileSearch}
                labelA="No"
                labelB="Yes"
                onClick={toggleUseFileSearch}
                disabled={false} />

              <Toggle id={"UseDecisionServices"}
                labelText={"Use Decision Services"}
                toggled={useDecisionServices}
                labelA="No"
                labelB="Yes"
                onClick={toggleUseDecisionServices}
                disabled={false} />

              {/* <div>
                {agentModelClassName && <Select id="select-model-class-name"
                  value={agentModelClassName}
                  labelText="LLM"
                  onChange={(e) => changeModelClassName(e)}>
                  {modelClassNames.map((modelClassName, i) => (<SelectItem key={i} value={modelClassName.value} text={modelClassName.name} />))}
                </Select>}
                <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

                {agentModelName && <Select id="select-model-name"
                  value={agentModelName}
                  labelText="Model Name"
                  onChange={(e) => changeModelName(e)}>
                  {modelClassNames.find((modelClassName) => (modelClassName.value === agentModelClassName))?.modelNames.map((modelName, i) => (<SelectItem key={i} value={modelName} text={modelName} />))}
                </Select>}
                <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
              </div> */}

            </Stack>
          </AccordionItem>
          <AccordionItem key="2" title="Documents" className="owl-agent-config-accordion-item" open={showDocuments} onClick={() => { setShowSettings(false); setShowDocuments(true) }}>
            <p><a target="_blank" href="/IBUpolicies.pdf">IBU Policies document</a></p>
            <p><a target="_blank" href="/IBUpolicies-onepage.pdf">IBU Policies document (one page)</a></p>
            <p><a target="_blank" href="/DemoScenario.pdf">IBU Demo Scenario</a></p>
          </AccordionItem>
        </Accordion>
        <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem', height: '1rem' }} />

        <Button renderIcon={Reset} size="sm" kind="tertiary" onClick={() => { owlAgentRef.current.resetConversation() }}>{"Reset Conversation History"}</Button>

      </Column>
      <Column lg={12} md={6} sm={3} className="page__r5">
        {activeAgent && <OwlAgent ref={owlAgentRef} backendBaseAPI={env.backendBaseAPI} agent={activeAgent} useFileSearch={useFileSearch} useDecisionServices={useDecisionServices} openState={true} randomNumber={randomNumber} setError={setError} />}
      </Column>

      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        {error && (<ToastNotification role="alert" caption={error} timeout={5000} title="Error" subtitle="" />)}
      </Column>
    </Grid>
  );
}

export default AgentsPage;

'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Accordion, AccordionItem, Button, Column, Dropdown, DropdownSkeleton, Grid, MultiSelect, Stack, ToastNotification, Toggle } from '@carbon/react';
import { QuestionAndAnswer, Trusted } from '@carbon/pictograms-react';
import { Octokit } from '@octokit/core';
import { context } from '../providers';
import { getEnv } from '../env';
import { useTranslation } from 'react-i18next';
import { Reset, Save } from '@carbon/react/icons';
import OwlAgent from '../agents/OwlAgent';
import AgentModel from '../agents/AgentModel';

const octokitClient = new Octokit({});

function AgentsPage() {
  let env = context()?.env;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();
  const [agents, setAgents] = useState([]);
  const [tools, setTools] = useState([]);
  const [useFileSearch, setUseFileSearch] = useState(true);
  const [useDecisionServices, setUseDecisionServices] = useState(false);
  const [activeAgent, setActiveAgent] = useState(null);
  const [promptEnglishContent, setPromptEnglishContent] = useState("");
  const [randomNumber, setRandomNumber] = useState(0);
  const [runnerClassNames, setRunnerClassNames] = useState([]);
  const [toolSelectedItems, setToolSelectedItems] = useState({ selectedItems: [] });
  const [agentModelName, setAgentModelName] = useState("");
  const [agentModelClassName, setAgentModelClassName] = useState("");
  const [showSettings, setShowSettings] = useState(true);
  const [showDocuments, setShowDocuments] = useState(false);
  const [multiselectToolsKey, setMultiselectToolsKey] = useState("multi-select-tools");

  const { t, i18n } = useTranslation();

  const owlAgentRef = useRef();

  useEffect(() => {
    // Désactiver le défilement
    document.body.style.overflow = 'hidden';
    return () => {
      // Réactiver le défilement lors du démontage du composant
      document.body.style.overflow = 'auto';
    };
  }, []);
  useEffect(() => {
    // Désactiver le défilement
    document.body.style.overflow = 'hidden';
    return () => {
      // Réactiver le défilement lors du démontage du composant
      document.body.style.overflow = 'auto';
    };
  }, []);

  useEffect(() => {
    const loadData = async () => {
      const agents = await getAgents();
      const tools = await getTools();
      if (tools) {
        // Change tool names, add ** at the beginning of the name if the tool has a tag decision, add ++ if the tool has a tag rag
        const enhancedToolNames = tools.map(tool => {
          if (tool.tags.includes('decision')) {
            tool.tool_name = "*" + tool.tool_name;
          }
          if (tool.tags.includes('rag')) {
            tool.tool_name = "*" + tool.tool_name;
          }
          return tool;
        }).sort((a, b) => a.tool_name.localeCompare(b.tool_name));;
        setTools(enhancedToolNames);
        const prompts = await getPrompts();
        const agentsWithPrompts = await addPromptDetailsInAllAgents(agents, prompts);
        const agentsWithTools = agentsWithPrompts.map(agent => ({ ...agent, toolsData: agent.tools.map(tool => (enhancedToolNames.find(t => t.tool_id === tool))) }));

        setAgents(agentsWithTools);
        setActiveAgent(agentsWithTools[0]);
      } else {
        setAgents(agents);
        if (agents?.length > 0) {
          setActiveAgent(agents[0]);
        }
      }

      setRandomNumber(Math.floor(Math.random() * 1000000000));
    }

    try {
      if (!env?.backendBaseAPI) {
        env = getEnv();
      }
      loadData();
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (activeAgent) {
      setAgentModelName(activeAgent.modelName);
      setAgentModelClassName(activeAgent.modelClassName);
      setPromptEnglishContent(activeAgent.prompt_text);
      setToolSelectedItems({ selectedItems: activeAgent.toolsData });
      setMultiselectToolsKey("multi-select-tools-" + Date.now())
      // Check in activeAgent.tools if any tool id corresponds to a tool in tools that has the tag decision
      setUseDecisionServices(activeAgent.toolsData.some(tool => tool?.tags.includes('decision')));
      // Same with file search and tools that have the tag rag
      setUseFileSearch(activeAgent.toolsData.some(tool => tool?.tags.includes('rag')));
    }
  }, [activeAgent]);

  const getAgents = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/agents`);
      if (res.status === 200) {
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
        return res.data;
      } else {
        setError('Error obtaining agent data (' + res.status + ')');
      }
    } catch (error) {
      setError('Error obtaining agent data:' + error.message);
      console.error('Error obtaining agent data:', error);
    }
  }

  const getTools = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/tools`);
      if (res.status === 200) {
        return res.data;
      } else {
        setError('Error obtaining tool data (' + res.status + ')');
        console.error('Error obtaining tool data ', res);
      }
    } catch (error) {
      setError('Error obtaining tool data:' + error.message);
      console.error('Error obtaining tool data:' + error);
    }
  }

  const getPrompts = async () => {
    try {
      const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/prompts`);
      if (res.status === 200) {
        return res.data;
      } else {
        setError('Error obtaining prompt data (' + res.status + ')');
        console.error('Error obtaining prompt data ', res);
      }
    } catch (error) {
      setError('Error obtaining prompt data:' + error.message);
      console.error('Error obtaining prompt data:' + error);
    }
  }

  const addPromptDetailsInAllAgents = (agents, prompts) => {
    // For each agent, I need to check in prompts if it has a prompt_ref. If so, I need to check in locales if it has an 'en' locale. If so, I need to retrieve the text and put it in the agent so that I can display it in the component
    const agentsWithPrompts = agents.map(agent => {
      if (agent.prompt_ref) {
        const prompt = prompts?.find(prompt => prompt.prompt_id === agent.prompt_ref);
        if (prompt) {
          const locale = prompt.locales.find(locale => locale.locale === 'en');
          if (locale) {
            agent.prompt_text = locale.text;
          }
        }
      }
      return agent;
    });
    return agentsWithPrompts;
  }

  const updateAgent = async () => {
    // If this is is the first time the agent is being updated, we need to create a temporary agent object with the same name and runner_class_name as the active agent
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
    agentToUpdate.tools = toolSelectedItems.selectedItems.map(tool => tool.tool_id);
    agentToUpdate.toolsData = [...toolSelectedItems.selectedItems];

    // Update the agent in the backend
    try {
      const res = await octokitClient.request(
        action + env.backendBaseAPI + "a/agents/" + (firstTimeUpdate ? "" : agentId), {
        agent_id: agentId,
        name: agentToUpdate.name,
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

  const toggleUseDecisionServices = () => {
    const newUseDecisionServices = !useDecisionServices;
    if (newUseDecisionServices) {
      // Add all tools with tags that contain 'decision'
      const newToolSelectedItems = toolSelectedItems.selectedItems;
      tools.forEach(tool => {
        if (tool.tags.includes('decision')) {
          if (!newToolSelectedItems.includes(tool)) {
            newToolSelectedItems.push(tool);
          }
        }
      });
      setToolSelectedItems({ selectedItems: newToolSelectedItems });
    } else {
      // Remove all tools with tags that contain 'decision'
      const newToolSelectedItems = toolSelectedItems.selectedItems.filter(tool => !tool.tags.includes('decision'));
      setToolSelectedItems({ selectedItems: newToolSelectedItems });
    }
    setUseDecisionServices(newUseDecisionServices);
    setMultiselectToolsKey("multi-select-tools-" + Date.now())
  }

  const toggleUseFileSearch = () => {
    const newUseFileSearch = !useFileSearch;
    if (newUseFileSearch) {
      // Add all tools with tags that contain 'rag'
      const newToolSelectedItems = toolSelectedItems.selectedItems;
      tools.forEach(tool => {
        if (tool.tags.includes('rag')) {
          if (!newToolSelectedItems.includes(tool)) {
            newToolSelectedItems.push(tool);
          }
        }
      });
      setToolSelectedItems({ selectedItems: newToolSelectedItems });
    } else {
      // Remove all tools with tags that contain 'rag'
      const newToolSelectedItems = toolSelectedItems.selectedItems.filter(tool => !tool.tags.includes('rag'));
      setToolSelectedItems({ selectedItems: newToolSelectedItems });
    }
    setUseFileSearch(newUseFileSearch);
    setMultiselectToolsKey("multi-select-tools-" + Date.now())
  }

  const updateUseDecisionServicesToggle = (selection) => {
    const newUseDecisionServices = selection.selectedItems.some(tool => tool.tags.includes('decision'));
    setUseDecisionServices(newUseDecisionServices);
  }

  const updateUseFileSearchToggle = (selection) => {
    const newUseFileSearch = selection.selectedItems.some(tool => tool.tags.includes('rag'));
    setUseFileSearch(newUseFileSearch);
  }

  return (
    <Grid condensed>
      {/*<Column lg={16} md={8} sm={4} className="landing-page__banner" style={{ paddingBottom: "1rem" }}>
        <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start" }}>
          <QuestionAndAnswer style={{ width: '5rem', height: 'auto', padding: "0.5rem" }} />
          <h1 className="landing-page__heading" style={{ marginLeft: "2rem" }}>%Title%</h1>
        </div>
      </Column>*/}

      <Column lg={4} md={2} sm={1} className="page__r4">
        {loading || !activeAgent && (<DropdownSkeleton />)}
        {!loading && activeAgent && <Dropdown id={"agentId"}
          titleText={"Agent"}
          items={agents}
          itemToString={(item) => (item ? item.name ? item.name : item.agent_id : "")}
          selectedItem={activeAgent}
          onChange={(e) => setActiveAgent(e.selectedItem)}
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

              <AgentModel agentModelClassName={agentModelClassName} setAgentModelClassName={setAgentModelClassName} agentModelName={agentModelName} setAgentModelName={setAgentModelName} />

              {loading || !activeAgent && (<DropdownSkeleton />)}
              {!loading && activeAgent && (<MultiSelect id="multi-select-tools"
                key={multiselectToolsKey}
                label="Tools"
                selectionFeedback="fixed"
                titleText="Tools"
                useTitleInItem={true}
                items={tools}
                itemToString={(item) => (item ? item.tool_name : "")}
                initialSelectedItems={toolSelectedItems.selectedItems}
                onChange={(selection) => { setToolSelectedItems(selection); updateUseDecisionServicesToggle(selection); updateUseFileSearchToggle(selection) }} />)
              }

              <Button renderIcon={Save} kind="primary" onClick={updateAgent}>{"Apply changes"}</Button>
            </Stack>
          </AccordionItem>
          <AccordionItem key="2" title="Documents" className="owl-agent-config-accordion-item" open={showDocuments} onClick={() => { setShowSettings(false); setShowDocuments(true) }}>
            <p><a target="_blank" href="/IBUpolicies.pdf">IBU Policies document</a></p>
            <p><a target="_blank" href="/DemoScenario.pdf">IBU Demo Scenario</a></p>
          </AccordionItem>
        </Accordion>
        <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem', height: '1rem' }} />

        <Button renderIcon={Reset} size="sm" kind="tertiary" onClick={() => { owlAgentRef.current.resetConversation() }}>{"Reset Conversation"}</Button>

      </Column>
      <Column lg={12} md={6} sm={3} className="page__r5">
        {activeAgent && <OwlAgent ref={owlAgentRef} backendBaseAPI={env.backendBaseAPI} agent={activeAgent} promptEnglishContent={promptEnglishContent} useFileSearch={useFileSearch} useDecisionServices={useDecisionServices} openState={true} randomNumber={randomNumber} setError={setError} />}
      </Column>

      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        {error && (<ToastNotification role="alert" caption={error} timeout={5000} title="Error" subtitle="" />)}
      </Column>
    </Grid>
  );
}

export default AgentsPage;

import { Button, Dropdown, DropdownSkeleton, Modal, MultiSelect, NumberInput, Popover, PopoverContent, Select, SelectItem, TextArea, TextInput, Toggle } from '@carbon/react';
import React, { useEffect, useState } from 'react';
import { AiGovernancePrompt, WatsonxData } from '@carbon/pictograms-react';
import { Octokit } from '@octokit/core';
import { View } from '@carbon/react/icons';
import { useTranslation } from 'react-i18next';
import AgentModel from './AgentModel';
import AgentTools from './AgentTools';

const octokitClient = new Octokit({});

const Agent = ({ backendBaseAPI, mode, agent, agents, prompts, runnerClassNames, modelClassNames, openState, setOpenState, onSuccess, setError }) => {
    // mode = 'create' or 'edit'
    const [loading, setLoading] = useState(true);
    const [empty, setEmpty] = useState(false);
    const [agentId, setAgentId] = useState("");
    const [agentName, setAgentName] = useState("");
    const [agentDescription, setAgentDescription] = useState("");
    const [agentModelName, setAgentModelName] = useState("");
    const [agentModelClassName, setAgentModelClassName] = useState("langchain_openai.ChatOpenAI");
    const [agentRunnerClassName, setAgentRunnerClassName] = useState("athena.llm.agents.agent_mgr.OwlAgentDefaultRunner");
    const [currentItemPromptRef, setCurrentItemPromptRef] = useState();
    const [agentTemperature, setAgentTemperature] = useState(0);
    const [agentTopK, setAgentTopK] = useState(1);
    const [agentTopP, setAgentTopP] = useState(1);
    const [toolSelectedItems, setToolSelectedItems] = useState({ selectedItems: [] });
    const [hiddenToUI, setHiddenToUI] = useState(false);

    const [dropdownItemsPromptRef, setDropdownItemsPromptRef] = useState([]);

    const [open, setOpen] = useState(false);

    const { t, i18n } = useTranslation();

    useEffect(() => {
        if (mode === 'edit') {
            setAgentId(agent.agent_id);
            setAgentName(agent.name);
            setAgentDescription(agent.description);
            setAgentRunnerClassName(agent.runner_class_name);

            if (modelClassNames && modelClassNames.length > 0) {
                // Check agent.modelClassName and agent.modelName
                const modelClassName = modelClassNames.find((modelClassName) => (modelClassName.value === agent.modelClassName));
                if (modelClassName) {
                    setAgentModelClassName(agent.modelClassName);
                    // agent.modelClassName is valid
                    if (modelClassName.modelNames.find((modelName) => (modelName === agent.modelName))) {
                        // agent.modelName is valid
                        setAgentModelName(agent.modelName);
                    } else {
                        // agent.modelName is invalid, select the first model name
                        setAgentModelName(modelClassName.modelNames[0]);
                    }
                } else {
                    // agent.modelClassName is invalid, select the first model class name and the first model name
                    setAgentModelClassName(modelClassNames[0].value);
                    setAgentModelName(modelClassNames[0].modelNames[0]);
                }
            } else {
                setAgentModelClassName(agent.modelClassName);
                setAgentModelName(agent.modelName);
            }
            setCurrentItemPromptRef({ "selectedItem": agent.prompt_ref });
            setAgentTemperature(agent.temperature);
            setAgentTopK(agent.top_k);
            setAgentTopP(agent.top_p);
            setToolSelectedItems({ selectedItems: [...agent.tools] });
            setHiddenToUI(agent.hidden_to_ui);
        } else {
            setCurrentItemPromptRef("");
            setToolSelectedItems({ selectedItems: [] });
        }
        setEmpty(false)
    }, [agent]);

    useEffect(() => {
        setLoading(true);
        try {
            const items = prompts.map(prompt => (prompt.prompt_id));
            setDropdownItemsPromptRef(["", ...items]);
        } finally {
            setLoading(false);
        }
    }, [prompts]);

    const upsertAgent = async (mode) => {
        let ed = (mode === "create" ? "created" : "updated");
        let ing = (mode === "create" ? "creating" : "updating");

        try {
            const res = await octokitClient.request(
                (mode === "create" ? "POST " : "PUT ") + backendBaseAPI + "a/agents" + (mode === "edit" ? "/" + agentId : ""), {
                agent_id: agentId,
                name: agentName,
                description: agentDescription,
                modelName: agentModelName,
                modelClassName: agentModelClassName,
                runner_class_name: agentRunnerClassName,
                prompt_ref: currentItemPromptRef.selectedItem || (mode === "create" ? "" : agent.prompt_ref),
                temperature: parseInt(agentTemperature),
                top_k: parseInt(agentTopK),
                top_p: parseInt(agentTopP),
                tools: toolSelectedItems.selectedItems || (mode === "create" ? [] : agent.tools),
                hidden_to_ui: hiddenToUI
            });

            if (res.status === 200) {
                console.log(`Agent ${ed}`, res.data);
                onSuccess();
            } else {
                setError(`Error ${ing} agent (` + res.status + ')');
                console.error(`Error ${ing} agent`, res);
            }
        }
        catch (error) {
            setError(`Error ${ing} agent: ` + error.message);
            console.error(`Error ${ing} agent`, error);
        }
    }

    const onRequestSubmit = () => {
        if (!agentName) {
            setEmpty(true);
        } else {
            upsertAgent(mode);

            setAgentId("");
            setAgentName("");
            setAgentDescription("");
            setAgentRunnerClassName("athena.llm.agents.agent_mgr.OwlAgentAbstractRunner");
            setAgentModelClassName("langchain_openai.ChatOpenAI");
            setAgentModelName("");
            setCurrentItemPromptRef("");
            setAgentTemperature(0);
            setAgentTopK(1);
            setAgentTopP(1);
            setToolSelectedItems({ selectedItems: [] });
            setHiddenToUI(false);

            setOpenState(false);
        }
    }

    const checkAndBuildId = (e) => {
        setEmpty(!e.target.value);
        setAgentName(e.target.value);
        if (mode === "create") {
            let value = e.target.value.replace(/[^a-zA-Z0-9_À-ÿ]/g, '_').toLowerCase();
            let unique = true;
            do {
                unique = agents.filter((t) => t.agent_id === value).length === 0;

                if (unique) {
                    setAgentId(value);
                    break;
                }
                value += "_";
            }
            while (!unique)
        }
    }

    return (
        <Modal open={openState}
            onRequestClose={() => setOpenState(false)}
            modalHeading={(mode == "create" ? "Create a new agent" : "Update agent " + agentId)}
            modalLabel="Agents"
            primaryButtonText={(mode == "create" ? "Add" : "Update")}
            secondaryButtonText="Cancel"
            preventCloseOnClickOutside
            shouldSubmitOnEnter
            onRequestSubmit={onRequestSubmit}>
            <p style={{ marginBottom: '1rem' }}>
                {(mode == "create" ? "Add a new agent to your Owl Agent framework." : "Update the agent information.")}
            </p>
            <WatsonxData style={{ width: '5rem', height: 'auto', padding: "0.5rem" }} />

            <TextInput data-modal-primary-focus id="text-agent-name"
                labelText="Agent name"
                placeholder="e.g. IBU new agent"
                invalid={empty}
                invalidText="This field cannot be empty"
                value={agentName}
                onChange={checkAndBuildId} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextArea id="text-agent-description"
                labelText="Description"
                value={agentDescription}
                onChange={(e) => setAgentDescription(e.target.value)}
                placeholder="e.g. This is the new IBU agent that uses LLM and Business Rules to make intelligent decisions..." />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <Toggle id="toggle-hidden-to-ui"
                labelText="Hidden to UI"
                labelA="No"
                labelB="Yes"
                onToggle={(e) => setHiddenToUI(e)} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <Select id="select-runner-class-name"
                value={agentRunnerClassName}
                labelText="Runner Class Name"
                onChange={(e) => setAgentRunnerClassName(e.target.value)}>
                <SelectItem value="" text="" />
                {runnerClassNames.map((runnerClassName, i) => (<SelectItem key={i} value={runnerClassName.value} text={runnerClassName.name} />))}
            </Select>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <AgentModel modelClassNames={modelClassNames} agentModelClassName={agentModelClassName} setAgentModelClassName={setAgentModelClassName} agentModelName={agentModelName} setAgentModelName={setAgentModelName} setError={setError} />

            <NumberInput id="carbon-number-temperature"
                value={agentTemperature}
                helperText="Enter an integer number between 0 and 100. 
                    This parameter influences the language model's output, determining whether the output is more creative or predictable. 
                    The higher the temperature, the more creative and diverse the outputs tend to be."
                min={0} max={100}
                label="Temperature"
                invalidText="Number is not valid"
                onChange={(e) => setAgentTemperature(e.target.value)} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <NumberInput id="carbon-number-top-k"
                value={agentTopK}
                helperText="Enter an integer number between 0 and 50. 
                    This parameter refers to a sampling technique used during text generation. 
                    When the model is prompted to generate the next word in a sequence, 
                    the top-K sampling method limits the selection to the K most likely next words based on their probabilities. 
                    This means that only the K most probable tokens are considered for the next word, 
                    providing a way to control the diversity and randomness of the generated text. 
                    For example, a top-K of 1 means that the next selected token is the most probable among all, 
                    while a higher top-K value allows for a wider range of possibilities by considering more potential tokens for the next word."
                min={0} max={50}
                label="Top-K"
                invalidText="Number is not valid"
                onChange={(e) => setAgentTopK(e.target.value)} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <NumberInput id="carbon-number-top-p"
                value={agentTopP}
                helperText="Enter an integer number between 0 and 50. 
                    Top-P (also known as nucleus sampling) is a parameter that controls the diversity of the generated text. 
                    It acts as a cumulative probability cutoff for token selection, 
                    meaning that lower values of top-P result in sampling from a smaller, more top-weighted set of tokens. 
                    Essentially, top-P sampling allows the model to consider a subset of the most probable tokens, 
                    thereby influencing the diversity and randomness of the generated text based on the specified threshold value."
                min={0} max={50}
                label="Top-P"
                invalidText="Number is not valid"
                onChange={(e) => setAgentTopP(e.target.value)} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            {loading && (<DropdownSkeleton />)}
            {!loading && (<>
                <Dropdown
                    key={Math.random().toString()}
                    id="drop-down-prompt-ref"
                    label="Prompt Ref"
                    titleText="Prompt Ref"
                    items={dropdownItemsPromptRef}
                    onChange={(selectedItem) => setCurrentItemPromptRef(selectedItem)}
                    initialSelectedItem={currentItemPromptRef && currentItemPromptRef.selectedItem} />
                {currentItemPromptRef && currentItemPromptRef.selectedItem &&
                    <Popover align="bottom-left" isTabTip title="Display Prompt" open={open}
                        onKeyDown={(evt) => { if (evt.key === "Escape") { setOpen(false); evt.stopPropagation(); } }}
                        onRequestClose={() => setOpen(false)}>
                        <Button renderIcon={View} iconDescription="View prompt" hasIconOnly kind="ghost" onClick={() => setOpen(!open)} />
                        <PopoverContent className="card-popover-content card-popover-dark-background">
                            <AiGovernancePrompt style={{ padding: "0.5rem" }} />
                            {prompts.filter(prompt => prompt.prompt_id === currentItemPromptRef.selectedItem).map((prompt, i) => (
                                <div key={i} className="card-detail-large">
                                    <div className="card-detail">Prompt Name: {prompt.name}</div>
                                    {prompt.locales.map((locale, j) => (
                                        <div className="card-popover-content-block">
                                            <div className="card-name">{locale.locale}</div>
                                            <div className="card-description" dangerouslySetInnerHTML={{ __html: locale.text.replace(/\n/g, "<br/>") }} />
                                        </div>
                                    ))}
                                </div>))}
                        </PopoverContent>
                    </Popover>}
            </>)}
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem', height: '1rem' }} />

            <AgentTools backendBaseAPI={backendBaseAPI} toolSelectedItems={toolSelectedItems} setToolSelectedItems={setToolSelectedItems} setError={setError} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem', height: '10rem' }} />
        </Modal >
    )
};

export default Agent;
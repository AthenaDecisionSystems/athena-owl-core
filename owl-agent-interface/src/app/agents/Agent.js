import { Button, Dropdown, DropdownSkeleton, Modal, MultiSelect, NumberInput, Popover, PopoverContent, Select, SelectItem, TextArea, TextInput } from '@carbon/react';
import React, { useEffect, useState } from 'react';
import { AiGovernancePrompt, WatsonxData } from '@carbon/pictograms-react';
import { Octokit } from '@octokit/core';
import { View } from '@carbon/react/icons';

const octokitClient = new Octokit({});

const Agent = ({ backendBaseAPI, mode, agent, agents, openState, setOpenState, onSuccess, setError }) => {
    // mode = 'create' or 'edit'
    const [loading, setLoading] = useState(true);
    const [empty, setEmpty] = useState(false);
    const [agentId, setAgentId] = useState("");
    const [agentName, setAgentName] = useState("");
    const [agentDescription, setAgentDescription] = useState("");
    const [agentModelName, setAgentModelName] = useState("gpt-3.5-turbo");
    const [agentModelClassName, setAgentModelClassName] = useState("langchain_openai.ChatOpenAI");
    const [agentRunnerClassName, setAgentRunnerClassName] = useState("athena.llm.agents.agent_mgr.OwlAgentAbstractRunner");
    const [currentItemPromptRef, setCurrentItemPromptRef] = useState();
    const [agentTemperature, setAgentTemperature] = useState(0);
    const [agentTopK, setAgentTopK] = useState(1);
    const [agentTopP, setAgentTopP] = useState(1);
    const [toolSelectedItems, setToolSelectedItems] = useState({ selectedItems: [] });

    const [dropdownItemsPromptRef, setDropdownItemsPromptRef] = useState([]);
    const [dropdownItemsTools, setDropdownItemsTools] = useState([]);
    const [promptList, setPromptList] = useState([]);

    const [open, setOpen] = useState(false);

    useEffect(() => {
        if (mode === 'edit') {
            setAgentId(agent.agent_id);
            setAgentName(agent.name);
            setAgentDescription(agent.description);
            setAgentModelName(agent.modelName);
            setAgentModelClassName(agent.modelClassName);
            setAgentRunnerClassName(agent.runner_class_name);
            setCurrentItemPromptRef({ "selectedItem": agent.prompt_ref });
            setAgentTemperature(agent.temperature);
            setAgentTopK(agent.top_k);
            setAgentTopP(agent.top_p);
            setToolSelectedItems({ selectedItems: [...agent.tools] });
        } else {
            setCurrentItemPromptRef("");
            setToolSelectedItems({ selectedItems: [] });
        }
        setEmpty(false)
    }, [agent]);

    useEffect(() => {
        // Preload tools & prompts
        async function getTools() {
            try {
                const res = await octokitClient.request(`GET ${backendBaseAPI}a/tools`);
                if (res.status === 200) {
                    const items = res.data.map(tool => (tool.tool_id));
                    setDropdownItemsTools(items);
                } else {
                    setError('Error obtaining tool data (' + res.status + ')');
                    console.error('Error obtaining tool data ', res);
                }
            } catch (error) {
                setError('Error obtaining tool data:' + error.message);
                console.error('Error obtaining tool data:' + error);
            }
            setLoading(false);
        }

        async function getPrompts() {
            try {
                const res = await octokitClient.request(`GET ${backendBaseAPI}a/prompts`);
                if (res.status === 200) {
                    const items = res.data.map(prompt => (prompt.name));
                    setDropdownItemsPromptRef(["", ...items]);
                    setPromptList(res.data);
                } else {
                    setError('Error obtaining prompt data (' + res.status + ')');
                    console.error('Error obtaining prompt data ', res);
                }
            } catch (error) {
                setError('Error obtaining prompt data:' + error.message);
                console.error('Error obtaining prompt data:' + error);
            }
            setLoading(false);
        }

        getTools();
        getPrompts();
    }, []);

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
                tools: toolSelectedItems.selectedItems || (mode === "create" ? [] : agent.tools)
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
            setAgentModelName("gpt-3.5-turbo");
            setAgentModelClassName("");
            setAgentRunnerClassName("athena.llm.agents.agent_mgr.OwlAgentAbstractRunner");
            setCurrentItemPromptRef("");
            setAgentTemperature(0);
            setAgentTopK(1);
            setAgentTopP(1);
            setToolSelectedItems({ selectedItems: [] });

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

            <TextInput data-modal-primary-focus id="text-input-1"
                labelText="Agent name"
                placeholder="e.g. IBU new agent"
                invalid={empty}
                invalidText="This field cannot be empty"
                value={agentName}
                onChange={checkAndBuildId} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextArea id="text-area-1"
                labelText="Description"
                value={agentDescription}
                onChange={(e) => setAgentDescription(e.target.value)}
                placeholder="e.g. This is the new IBU agent that uses LLM and Business Rules to make intelligent decisions..." />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextInput id="text-model-class-name"
                value={agentModelClassName}
                labelText="Model Class Name"
                onChange={(e) => setAgentModelClassName(e.target.value)}>
            </TextInput>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <Select id="select-class-name"
                defaultValue={agentRunnerClassName}
                labelText="Runner Class Name"
                onChange={(e) => setAgentRunnerClassName(e.target.value)}>
                <SelectItem value="" text="" />
                <SelectItem
                    value="athena.llm.agents.agent_mgr.OwlAgentAbstractRunner"
                    text="athena.llm.agents.agent_mgr.OwlAgentAbstractRunner" />
            </Select>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <Select id="select-model-name"
                defaultValue={agentModelName}
                labelText="Model Name"
                onChange={(e) => setAgentModelName(e.target.value)}>
                <SelectItem value="" text="" />
                <SelectItem
                    value="gpt-3.5-turbo"
                    text="GPT-3.5-turbo" />
                <SelectItem
                    value="gpt-4-turbo"
                    text="GPT-4-turbo" />
                <SelectItem
                    value="gpt-4o"
                    text="GPT-4o" />
            </Select>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

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
                            {promptList.filter(prompt => prompt.name === currentItemPromptRef.selectedItem).map((prompt, i) => (
                                <div key={i} className="card-detail-large">
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

            {loading && (<DropdownSkeleton />)}
            {!loading && (<MultiSelect id="multi-select-tools"
                key={toolSelectedItems.selectedItems.join(",")}
                label="Tools"
                titleText="Tools"
                items={dropdownItemsTools}
                initialSelectedItems={toolSelectedItems.selectedItems}
                onChange={(selection) => setToolSelectedItems(selection)}
                selectionFeedback="top-after-reopen" />)
            }
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem', height: '3rem' }} />
        </Modal >
    )
};

export default Agent;
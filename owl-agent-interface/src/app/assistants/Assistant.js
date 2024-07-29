import { DropdownSkeleton, Modal, MultiSelect, Select, SelectItem, TextArea, TextInput } from '@carbon/react';
import React, { useEffect, useState } from 'react';
import { QuestionAndAnswer } from '@carbon/pictograms-react';
import { Octokit } from '@octokit/core';
import { useEnv } from '../providers';
import { getEnv } from '../env';

const octokitClient = new Octokit({});

const Assistant = ({ mode, assistant, assistants, openState, setOpenState, onSuccess, setError }) => {
    let env = useEnv();

    // mode = 'create' or 'edit'
    const [loading, setLoading] = useState(true);
    const [empty, setEmpty] = useState(false);
    const [assistantId, setAssistantId] = useState("");
    const [assistantName, setAssistantName] = useState("");
    const [assistantDescription, setAssistantDescription] = useState("");
    const [className, setClassName] = useState("athena.llm.assistants.BaseAssistant.BaseAssistant");
    const [dropdownItems, setDropdownItems] = useState([]);
    const [agentSelectedItems, setAgentSelectedItems] = useState({ selectedItems: [] });

    useEffect(() => {
        if (mode === 'edit') {
            setAssistantId(assistant.assistant_id);
            setAssistantName(assistant.name);
            setAssistantDescription(assistant.description);
            setClassName(assistant.class_name);
            setAgentSelectedItems({ selectedItems: [...assistant.agents] });
        } else {
            setAgentSelectedItems({ selectedItems: [] });
        }
        setEmpty(false);
    }, [assistant]);

    useEffect(() => {
        // Preload agents
        async function getAgents() {
            try {
                const res = await octokitClient.request(`GET ${env.backendBaseAPI}a/agents`);
                if (res.status === 200) {
                    const items = res.data.map(agent => (agent.agent_id));
                    setDropdownItems(items);
                } else {
                    setError('Error obtaining agent data (' + res.status + ')');
                    console.error('Error obtaining agent data ', res);
                }
            } catch (error) {
                setError('Error obtaining agent data:' + error.message);
                console.error('Error obtaining agent data:' + error.message);
            }
            setLoading(false);
        }

        if (!env.backendBaseAPI) {
            getEnv().then((e) => {
                env = e;
                getAgents();
            })
        } else {
            getAgents();
        }
    }, []);

    const upsertAssistant = async (mode) => {
        let ed = (mode === "create" ? "created" : "updated");
        let ing = (mode === "create" ? "creating" : "updating");

        try {
            const res = await octokitClient.request(
                (mode === "create" ? "POST " : "PUT ") + env.backendBaseAPI + "a/assistants" + (mode === "edit" ? "/" + assistantId : ""), {
                assistant_id: assistantId,
                name: assistantName,
                description: assistantDescription,
                class_name: className,
                agents: agentSelectedItems.selectedItems || (mode === "create" ? "" : assistant.agents)
            });

            if (res.status === 200) {
                console.log(`Assistant ${ed}`, res.data);
                onSuccess();
            } else {
                setError(`Error ${ing} assistant (` + res.status + ')');
                console.error(`Error ${ing} assistant`, res);
            }
        }
        catch (error) {
            setError(`Error ${ing} assistant: ` + error.message);
            console.error(`Error ${ing} assistant`, error);
        }
    }

    const onRequestSubmit = () => {
        if (!assistantName) {
            setEmpty(true);
        } else {
            upsertAssistant(mode);
            setAssistantId("");
            setAssistantName("");
            setAssistantDescription("");
            setClassName("athena.llm.assistants.BaseAssistant.BaseAssistant");
            setAgentSelectedItems({ selectedItems: [] });

            setOpenState(false);
        }
    }

    const checkAndBuildId = (e) => {
        setEmpty(!e.target.value);
        setAssistantName(e.target.value);
        if (mode === "create") {
            let value = e.target.value.replace(/[^a-zA-Z0-9_À-ÿ]/g, '_').toLowerCase();
            let unique = true;
            do {
                unique = assistants.filter((t) => t.assistant_id === value).length === 0;

                if (unique) {
                    setAssistantId(value);
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
            modalHeading={(mode == "create" ? "Create a new assistant" : "Update assistant " + assistantId)}
            modalLabel="Assistants"
            primaryButtonText={(mode == "create" ? "Add" : "Update")}
            secondaryButtonText="Cancel"
            preventCloseOnClickOutside
            shouldSubmitOnEnter
            onRequestSubmit={onRequestSubmit}>
            <p style={{ marginBottom: '1rem' }}>
                {(mode == "create" ? "Add a new assistant to your Owl Agent framework." : "Update the assistant information.")}
            </p>
            <QuestionAndAnswer style={{ width: '5rem', height: 'auto', padding: "0.5rem" }} />

            <TextInput data-modal-primary-focus id="text-input-1"
                labelText="Assistant name"
                placeholder="e.g. IBU new assistant"
                invalid={empty}
                invalidText="This field cannot be empty"
                value={assistantName}
                onChange={checkAndBuildId} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextArea id="text-area-1"
                labelText="Description"
                value={assistantDescription}
                onChange={(e) => setAssistantDescription(e.target.value)}
                placeholder="e.g. This is the new IBU assistant that uses LLM and Business Rules to make intelligent decisions..." />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <Select id="select-class-name"
                defaultValue={className}
                labelText="Class Name"
                onChange={(e) => setClassName(e.target.value)}>
                <SelectItem value="" text="" />
                <SelectItem
                    value="athena.llm.assistants.BaseAssistant.BaseAssistant"
                    text="athena.llm.assistants.BaseAssistant.BaseAssistant" />
            </Select>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            {loading && (<DropdownSkeleton />)}
            {!loading && (<MultiSelect id="multi-select-agents"
                key={agentSelectedItems.selectedItems.join(",")}
                label="Agents"
                titleText="Agents"
                items={dropdownItems}
                initialSelectedItems={agentSelectedItems.selectedItems}
                onChange={(selection) => setAgentSelectedItems(selection)}
                selectionFeedback="top-after-reopen" />)
            }
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
        </Modal>
    )
};

export default Assistant;
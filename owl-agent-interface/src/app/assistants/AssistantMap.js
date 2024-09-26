import React, { useEffect, useState } from 'react';
import { AspectRatio, Column, OverflowMenu, OverflowMenuItem, Popover, PopoverContent, IconButton, SkeletonText } from '@carbon/react';
import { QuestionAndAnswer } from '@carbon/pictograms-react';
import { Close } from '@carbon/react/icons';
import { Octokit } from '@octokit/core';
import Assistant from './Assistant';
import OwlAgent from './OwlAgent';
import { context } from '../providers';

const octokitClient = new Octokit({});

export const AssistantMap = ({ rows, setRows, setError, reloadAssistants }) => {
    const ctx = context();

    const [loading, setLoading] = useState(true);
    const [agents, setAgents] = useState([]);
    const [openPopoverTable, setOpenPopoverTable] = useState([]); // Double entry: row x agents per row
    const [editAssistant, setEditAssistant] = useState(-1);
    const [openEditAssistant, setOpenEditAssistant] = useState(false);
    const [owlAgent, setOwlAgent] = useState(-1);
    const [openOwlAgent, setOpenOwlAgent] = useState(false);

    useEffect(() => {
        let tab = new Array(rows.length).fill([]);
        rows.map((row, i) => (
            tab[i] = new Array(row.agents.length).fill(false)
        ))
        setOpenPopoverTable(tab);

        // Preload agents
        async function getAgents() {
            try {
                const res = await octokitClient.request(`GET ${ctx.env.backendBaseAPI}a/agents`);
                if (res.status === 200) {
                    setAgents(res.data);
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
        getAgents();
    }, [rows]);

    const displayPopoverTable = (assistantIndex, agentIndex, open) => {
        const newOpenPopoverTable = openPopoverTable.map((tab, i) => (
            tab.map((item, j) => ((i === assistantIndex) && (j === agentIndex) ? open : false))))
        setOpenPopoverTable(newOpenPopoverTable);
    }

    if (loading) {
        return (
            <>
                {rows.map((row, i) => (<Column key={i} lg={3} md={2} sm={2} >
                    <SkeletonText className="card" />
                </Column>))}
            </>
        );
    }

    const deleteAssistant = async (index) => {
        try {
            const res = await octokitClient.request(
                `DELETE ${ctx.env.backendBaseAPI}a/assistants/${rows[index].assistant_id}`
            );
            if (res.status === 200) {
                console.log('Assistant deleted', res.data);
                setRows((rows) => {
                    const newRows = [...rows];
                    newRows.splice(index, 1);
                    return newRows;
                });
            } else {
                setError('Error deleting assistant: ' + rows[index].assistant_id);
                console.error('Error deleting assistant', res);
            }
        } catch (error) {
            setError('Error deleting assistant: ' + error.message);
            console.error('Error deleting assistant', error);
        }
    }

    const startEdition = (index) => {
        setEditAssistant(index);
        setOpenEditAssistant(true);
    }

    const endEdition = () => {
        setEditAssistant(-1);
        reloadAssistants();
    }

    const startOwlAgent = (index) => {
        setOwlAgent(index);
        setOpenOwlAgent(true);
    }

    const endOwlAgent = () => {
        setOwlAgent(-1);
    }

    return (
        <>
            {(owlAgent !== -1) && (
                <OwlAgent assistant={rows[owlAgent]} openState={openOwlAgent} setOpenState={setOpenOwlAgent} randomNumber={Math.random()} />
            )}
            {(editAssistant !== -1) && (
                <Assistant mode="edit" assistant={rows[editAssistant]} assistants={rows} openState={openEditAssistant} setOpenState={setOpenEditAssistant} onSuccess={endEdition} setError={setError} />
            )}
            {rows.map((row, i) => (<Column key={i} lg={3} md={2} sm={2} >
                <AspectRatio className="card" ratio="4x3" onDoubleClick={() => startEdition(i)}>
                    <div className="card-header" >
                        <QuestionAndAnswer style={{ padding: "0.5rem" }} onClick={() => startOwlAgent(i)} style={{ cursor: "pointer" }} />
                        <OverflowMenu className="card-menu" >
                            <OverflowMenuItem itemText="Edit" onClick={() => startEdition(i)} />
                            <OverflowMenuItem itemText="Launch" onClick={() => startOwlAgent(i)} />
                            <OverflowMenuItem hasDivider isDelete itemText="Delete" onClick={() => deleteAssistant(i)} />
                        </OverflowMenu>
                    </div>
                    <div className="card-name">{row.name}</div>
                    <div className="card-item-id">{row.assistant_id}</div>
                    <div className="card-description">{row.description}</div>
                    <div className="card-class-name" title="Assistant's class name">{row.class_name}</div>

                    {(row.agents && row.agents.length > 0) && (
                        <div className="card-description">Agents:
                            <ul>
                                {row.agents.map((agentId, j) => (
                                    agents.filter(agent => agent.agent_id === agentId).map((agent, k) => (
                                        <li key={k}>
                                            <Popover title="Display agent details" align="bottom-left" open={openPopoverTable[i][j]} >
                                                <a style={{ cursor: "pointer" }} onClick={() => displayPopoverTable(i, j, true)}>{agentId}</a>
                                                <PopoverContent className="card-popover-content">
                                                    <IconButton label="Close" renderIcon={Close} align="top-right" kind="ghost" onClick={() => displayPopoverTable(i, j, false)} />
                                                    <div className="card-name">{agentId}</div>
                                                    <div className="card-name">{agent.name}</div>
                                                    <div className="card-class-name">Class name: {agent?.class_name}</div>
                                                    <div className="card-description">{agent?.description}</div>
                                                    <div className="card-detail">LLM: {agent?.modelName}</div>
                                                    <div className="card-detail">Prompt ref: {agent?.prompt_ref}</div>
                                                    <div className="card-detail">Temperature: {agent?.temperature}</div>
                                                    <div className="card-detail">Top K: {agent?.top_k}</div>
                                                    <div className="card-detail">Top P: {agent?.top_p}</div>
                                                    {(agent.tools && agent.tools.length > 0) && (
                                                        <div className="card-description">Tools:
                                                            <ul>
                                                                {agent.tools.map((tool, l) => (
                                                                    <li key={l}>{tool}</li>
                                                                ))}
                                                            </ul>
                                                        </div>)}
                                                </PopoverContent>
                                            </Popover>
                                        </li>
                                    ))))}
                            </ul>
                        </div>)}

                    {agents.filter(agent => agent.agent_id === row.agent_id).map((agent, j) => (
                        <div key={j} className="card-item-id">
                            Agent: <Popover title="Display agent details" align="bottom-left" open={openPopoverTable[i]} >
                                <a onClick={() => displayPopoverTable(i, true)}>{row.agent_id}</a>
                                <PopoverContent className="card-popover-content">
                                    <IconButton label="Close" renderIcon={Close} align="top-right" kind="ghost" onClick={() => displayPopoverTable(i, false)} />
                                    <div className="card-name">{row.agent_id}</div>
                                    <div className="card-name">{agent.name}</div>
                                    <div className="card-class-name">Class name: {agent?.class_name}</div>
                                    <div className="card-description">{agent?.description}</div>
                                    <div className="card-detail">LLM: {agent?.modelName}</div>
                                    <div className="card-detail">Prompt ref: {agent?.prompt_ref}</div>
                                    <div className="card-detail">Temperature: {agent?.temperature}</div>
                                    <div className="card-detail">Top K: {agent?.top_k}</div>
                                    <div className="card-detail">Top P: {agent?.top_p}</div>
                                    {(agent.tools && agent.tools.length > 0) && (
                                        <div className="card-description">Tools:
                                            <ul>
                                                {agent.tools.map((tool, j) => (
                                                    <li key={j}>{tool}</li>
                                                ))}
                                            </ul>
                                        </div>)}
                                </PopoverContent>
                            </Popover>
                        </div>))}
                </AspectRatio>
            </Column>
            ))
            }
        </>
    );
};

export default AssistantMap;

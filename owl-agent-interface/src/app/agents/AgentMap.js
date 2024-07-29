import React, { useEffect, useState } from 'react';
import { AspectRatio, Column, OverflowMenu, OverflowMenuItem, Popover, PopoverContent, IconButton } from '@carbon/react';
import { WatsonxData } from '@carbon/pictograms-react';
import { Close } from '@carbon/react/icons';
import { Octokit } from '@octokit/core';
import Agent from './Agent';
import { useEnv } from '../providers';

const octokitClient = new Octokit({});

export const AgentMap = ({ rows, setRows, setError, reloadAgents }) => {
    const env = useEnv();

    const [openPopoverLLMTable, setOpenPopoverLLMTable] = useState([]);
    const [openPopoverToolsTable, setOpenPopoverToolsTable] = useState([]);
    const [openPopoverPromptTable, setOpenPopoverPromptTable] = useState([]);
    const [editAgent, setEditAgent] = useState(-1);
    const [open, setOpen] = useState(false);

    useEffect(() => {
        setOpenPopoverLLMTable(new Array(rows.length).fill(false));
        setOpenPopoverToolsTable(new Array(rows.length).fill(false));
        setOpenPopoverPromptTable(new Array(rows.length).fill(false));
    }, [rows]);

    const displayPopoverLLMTable = (index, open) => {
        const newOpenPopoverLLMTable = openPopoverLLMTable.map((item, i) => (i === index ? open : false));
        setOpenPopoverLLMTable(newOpenPopoverLLMTable);
        if (open) {
            setOpenPopoverToolsTable(new Array(rows.length).fill(false));
            setOpenPopoverPromptTable(new Array(rows.length).fill(false));
        }
    }
    const displayPopoverToolsTable = (index, open) => {
        const newOpenPopoverToolsTable = openPopoverToolsTable.map((item, i) => (i === index ? open : false));
        setOpenPopoverToolsTable(newOpenPopoverToolsTable);
        if (open) {
            setOpenPopoverLLMTable(new Array(rows.length).fill(false));
            setOpenPopoverPromptTable(new Array(rows.length).fill(false));
        }
    }
    const displayPopoverPromptTable = (index, open) => {
        const newOpenPopoverPromptTable = openPopoverPromptTable.map((item, i) => (i === index ? open : false));
        setOpenPopoverPromptTable(newOpenPopoverPromptTable);
        if (open) {
            setOpenPopoverLLMTable(new Array(rows.length).fill(false));
            setOpenPopoverToolsTable(new Array(rows.length).fill(false));
        }
    }

    const deleteAgent = async (index) => {
        try {
            const res = await octokitClient.request(
                `DELETE ${env.backendBaseAPI}a/agents/${rows[index].agent_id}`
            );
            if (res.status === 200) {
                console.log('Agent deleted', res.data);
                setRows((rows) => {
                    const newRows = [...rows];
                    newRows.splice(index, 1);
                    return newRows;
                });
            } else {
                setError('Error deleting agent: ' + rows[index].agent_id);
                console.error('Error deleting agent', res);
            }
        } catch (error) {
            setError('Error deleting agent: ' + error.message);
            console.error('Error deleting agent', error);
        }
    }

    const startEdition = (index) => {
        setEditAgent(index);
        setOpen(true);
    }

    const endEdition = () => {
        setEditAgent(-1);
        reloadAgents();
    }

    return (
        <>
            {(editAgent !== -1) && (
                <Agent mode="edit" agent={rows[editAgent]} agents={rows} openState={open} setOpenState={setOpen} onSuccess={endEdition} setError={setError} />
            )}
            {rows.map((row, i) => (<Column key={i} lg={3} md={2} sm={2} >
                <AspectRatio className="card" ratio="4x3" onDoubleClick={() => startEdition(i)}>
                    <div className="card-header" >
                        <WatsonxData style={{ padding: "0.5rem" }} />
                        <OverflowMenu className="card-menu">
                            <OverflowMenuItem itemText="Edit" onClick={() => startEdition(i)} />
                            <OverflowMenuItem hasDivider isDelete itemText="Delete" onClick={() => deleteAgent(i)} />
                        </OverflowMenu>
                    </div>
                    <div className="card-name">{row.name}</div>
                    <div className="card-item-id">{row.agent_id}</div>
                    <div className="card-description">{row.description}</div>
                    <div className="card-class-name" title="Agent's class name">{row.class_name}</div>

                    <div className="card-item-id">
                        <Popover title="Display LLM parameters" align="bottom-left" open={openPopoverLLMTable[i]} >
                            <a style={{ cursor: "pointer" }} onClick={() => displayPopoverLLMTable(i, true)}>LLM Parameters</a>
                            <PopoverContent className="card-popover-content">
                                <IconButton label="Close" renderIcon={Close} align="top-right" kind="ghost" onClick={() => displayPopoverLLMTable(i, false)} />
                                <div className="card-detail-large">
                                    <div className="card-popover-content-block">
                                        <div className="card-detail">Model: {row.modelName}</div>
                                        <div className="card-detail">Temperature: {row.temperature}</div>
                                        <div className="card-detail">Top K: {row.top_k}</div>
                                        <div className="card-detail">Top P: {row.top_p}</div>
                                    </div>
                                </div>
                            </PopoverContent>
                        </Popover>
                    </div>

                    <div className="card-item-id">
                        <Popover title="Display Prompt" align="bottom-left" open={openPopoverPromptTable[i]} >
                            <a style={{ cursor: "pointer" }} onClick={() => displayPopoverPromptTable(i, true)}>Prompt</a>
                            <PopoverContent className="card-popover-content">
                                <IconButton label="Close" renderIcon={Close} align="top-right" kind="ghost" onClick={() => displayPopoverPromptTable(i, false)} />
                                <div className="card-detail-large">
                                    <div className="card-popover-content-block">
                                        <div className="card-detail">Prompt ref.:</div>
                                        <div className="card-class-name">{row.prompt_ref}</div>
                                        <div className="card-detail">Prompt:</div>
                                        <div className="card-description">Lorem ipsum dolor sit amet consectetur adipisicing elit. Autem nobis voluptatibus veritatis!</div>
                                    </div>
                                </div>
                            </PopoverContent>
                        </Popover>
                    </div>
                    {(row.tools && row.tools.length > 0) && (
                        <div className="card-item-id">
                            <Popover title="Display Tools" align="bottom-left" open={openPopoverToolsTable[i]} >
                                <a style={{ cursor: "pointer" }} onClick={() => displayPopoverToolsTable(i, true)}>Tools</a>
                                <PopoverContent className="card-popover-content">
                                    <IconButton label="Close" renderIcon={Close} align="top-right" kind="ghost" onClick={() => displayPopoverToolsTable(i, false)} />
                                    <div className="card-detail-large">
                                        <div className="card-popover-content-block">
                                            <div className="card-description">Tools:
                                                <ul>
                                                    {row.tools.map((tool, j) => (
                                                        <li key={j}>{tool}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </PopoverContent>
                            </Popover>
                        </div>)}
                </AspectRatio>
            </Column>
            ))}
        </>
    );
};

export default AgentMap;

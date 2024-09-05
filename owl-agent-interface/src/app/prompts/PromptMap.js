import React, { useEffect, useState } from 'react';
import { AspectRatio, Column, OverflowMenu, OverflowMenuItem, Popover, PopoverContent, IconButton } from '@carbon/react';
import { AiGovernancePrompt } from '@carbon/pictograms-react';
import { Close } from '@carbon/react/icons';
import { Octokit } from '@octokit/core';
import Prompt from './Prompt';

const octokitClient = new Octokit({});

export const PromptMap = ({ backendBaseAPI, rows, setRows, setError, reloadPrompts }) => {
    const [openPopoverTable, setOpenPopoverTable] = useState([]);
    const [editPrompt, setEditPrompt] = useState(-1);
    const [open, setOpen] = useState(false);

    useEffect(() => {
        setOpenPopoverTable(new Array(rows.length).fill(false));
    }, [rows]);

    const displayPopoverTable = (index, open) => {
        const newOpenPopoverTable = openPopoverTable.map((item, i) => (i === index ? open : false));
        setOpenPopoverTable(newOpenPopoverTable);
    }

    const deletePrompt = async (index) => {
        try {
            const res = await octokitClient.request(`DELETE ${backendBaseAPI}a/prompts/${rows[index].name}`);
            if (res.status === 200) {
                console.log('Prompt deleted', res.data);
                setRows((rows) => {
                    const newRows = [...rows];
                    newRows.splice(index, 1);
                    return newRows;
                });
            } else {
                setError('Error deleting prompt: ' + rows[index].name);
                console.error('Error deleting prompt', res);
            }
        } catch (error) {
            setError('Error deleting prompt: ' + error.message);
            console.error('Error deleting prompt', error);
        }
    }

    const startEdition = (index) => {
        setEditPrompt(index);
        setOpen(true);
    }

    const endEdition = () => {
        setEditPrompt(-1);
        reloadPrompts();
    }

    return (
        <>
            {(editPrompt !== -1) && (
                <Prompt backendBaseAPI={backendBaseAPI} mode="edit" prompt={rows[editPrompt]} prompts={rows} openState={open} setOpenState={setOpen} onSuccess={endEdition} setError={setError} />
            )}
            {rows.map((row, i) => (<Column key={i} lg={3} md={2} sm={2} >
                <AspectRatio className="card" ratio="4x3" onDoubleClick={() => startEdition(i)}>
                    <div className="card-header" >
                        <AiGovernancePrompt style={{ padding: "0.5rem" }} />
                        <OverflowMenu className="card-menu">
                            <OverflowMenuItem itemText="Edit" onClick={() => startEdition(i)} />
                            <OverflowMenuItem hasDivider isDelete itemText="Delete" onClick={() => deletePrompt(i)} />
                        </OverflowMenu>
                    </div>
                    <div className="card-description">{row.prompt_id}</div>
                    <div className="card-name">{row.name}</div>
                    {(row.locales && row.locales.length > 0) && (
                        <>
                            <div className="card-description">
                                <ul>
                                    {row.locales.map((locale, j) => (
                                        <li key={j}>{locale.locale}</li>
                                    ))}
                                </ul>
                            </div>

                            <div className="card-item-id">
                                <Popover title="Display prompts" align="bottom-left" open={openPopoverTable[i]} >
                                    <a style={{ cursor: "pointer" }} onClick={() => displayPopoverTable(i, true)}>Prompts</a>
                                    <PopoverContent className="card-popover-content">
                                        <IconButton label="Close" renderIcon={Close} align="top-right" kind="ghost" onClick={() => displayPopoverTable(i, false)} />
                                        {row.locales.map((locale, j) => (
                                            <div key={j} className="card">
                                                <div className="card-name">{locale.locale}</div>
                                                <div className="card-description">{locale.text}</div>
                                            </div>
                                        ))}
                                    </PopoverContent>
                                </Popover>
                            </div>
                        </>
                    )}
                </AspectRatio>
            </Column>
            ))}
        </>
    );
};

export default PromptMap;

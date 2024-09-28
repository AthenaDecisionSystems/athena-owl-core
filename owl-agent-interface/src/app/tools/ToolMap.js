import React, { useState } from 'react';
import { AspectRatio, Column, OverflowMenu, OverflowMenuItem, Popover, PopoverContent, IconButton } from '@carbon/react';
import { Tools } from '@carbon/pictograms-react';
import { Octokit } from '@octokit/core';
import Tool from './Tool';
import { context } from '../providers';

const octokitClient = new Octokit({});

export const ToolMap = ({ rows, setRows, setError, reloadTools }) => {
    const ctx = context();

    const [open, setOpen] = useState(false);
    const [editTool, setEditTool] = useState(-1);

    const deleteTool = async (index) => {
        try {
            const res = await octokitClient.request(
                `DELETE ${ctx.env.backendBaseAPI}a/tools/${rows[index].tool_id}`
            );
            if (res.status === 200) {
                console.log('Tool deleted', res.data);
                setRows((rows) => {
                    const newRows = [...rows];
                    newRows.splice(index, 1);
                    return newRows;
                });
            } else {
                setError('Error deleting tool: ' + rows[index].tool_id);
                console.error('Error deleting tool', res);
            }
        } catch (error) {
            setError('Error deleting tool: ' + error.message);
            console.error('Error deleting tool', error);
        }
    }

    const startEdition = (index) => {
        setEditTool(index);
        setOpen(true);
    }

    const endEdition = () => {
        setEditTool(-1);
        reloadTools();
    }

    return (
        <>
            {(editTool !== -1) && (
                <Tool mode="edit" tool={rows[editTool]} tools={rows} openState={open} setOpenState={setOpen} onSuccess={endEdition} setError={setError} />
            )}
            {rows.map((row, i) => (<Column key={i} lg={3} md={2} sm={2} >
                <AspectRatio className="card" ratio="4x3" onDoubleClick={() => startEdition(i)}>
                    <div className="card-header" >
                        <Tools style={{ padding: "0.5rem" }} />
                        <OverflowMenu className="card-menu">
                            <OverflowMenuItem itemText="Edit" onClick={() => startEdition(i)} />
                            <OverflowMenuItem hasDivider isDelete itemText="Delete" onClick={() => deleteTool(i)} />
                        </OverflowMenu>
                    </div>
                    <div className="card-name">{row.tool_name}</div>
                    <div className="card-id">{row.tool_id}</div>
                    <div className="card-label">Function name:</div>
                    <div className="card-id">{row.tool_fct_name}</div>

                    <div className="card-label">Class name:</div>
                    <div className="card-class-name">{row.tool_class_name}</div>

                    <div className="card-description">{row.tool_description}</div>
                    {row.tool_arg_schema_class && (
                        <div className="card-description"><pre>{JSON.stringify(row.tool_arg_schema_class, null, 2)}</pre></div>
                    )}
                </AspectRatio>
            </Column>
            ))}
        </>
    );
};

export default ToolMap;

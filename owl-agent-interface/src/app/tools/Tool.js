import { Modal, TextInput } from '@carbon/react';
import React, { useEffect, useRef, useState } from 'react';
import { Tools } from '@carbon/pictograms-react';
import { Octokit } from '@octokit/core';
import { context } from '../providers';

const octokitClient = new Octokit({});

const Tool = ({ mode, tool, tools, openState, setOpenState, onSuccess, setError }) => {
    let env = context()?.env;

    // mode = 'create' or 'edit'
    const [empty, setEmpty] = useState(false)
    const [toolId, setToolId] = useState("");
    const [toolName, setToolName] = useState("");
    const [toolDescription, setToolDescription] = useState("");
    const [toolClassName, setToolClassName] = useState("ibu.llm.tools.client_tools");
    const [toolFctName, setToolFctName] = useState("");
    const [toolArgSchemaClass, setToolArgSchemaClass] = useState(null);

    useEffect(() => {
        if (mode === 'edit') {
            setToolId(tool.tool_id);
            setToolName(tool.tool_name);
            setToolDescription(tool.tool_description);
            setToolClassName(tool.tool_class_name);
            setToolFctName(tool.tool_fct_name);
            setToolArgSchemaClass(tool.tool_arg_schema_class);
        }
    }, [tool]);

    const upsertTool = async (mode) => {
        let ed = (mode === "create" ? "created" : "updated");
        let ing = (mode === "create" ? "creating" : "updating");

        try {
            const res = await octokitClient.request(
                (mode === "create" ? "POST " : "PUT ") + env.backendBaseAPI + "a/tools/" + (mode === "edit" ? tool.tool_id : ""), {
                tool_id: toolId,
                tool_name: toolName,
                tool_description: toolDescription,
                tool_class_name: toolClassName,
                tool_fct_name: toolFctName,
                tool_arg_schema_class: toolArgSchemaClass
            });

            if (res.status === 200) {
                console.log(`Tool ${ed}`, res.data);
                onSuccess();
            } else {
                setError(`Error ${ing} tool (` + res.status + ')');
                console.error(`Error ${ing} tool`, res);
            }
        }
        catch (error) {
            setError(`Error ${ing} tool: ` + error.message);
            console.error(`Error ${ing} tool`, error);
        }
    }

    const onRequestSubmit = () => {
        if (!toolName) {
            setEmpty(true);
        } else {
            upsertTool(mode);

            setToolId("");
            setToolName("");
            setToolDescription("");
            setToolClassName("ibu.llm.tools.client_tools");
            setToolFctName("");
            setToolArgSchemaClass(null);

            setOpenState(false);
        }
    }

    const checkAndBuildId = (e) => {
        setEmpty(!e.target.value);
        setToolName(e.target.value);
        if (mode === "create") {
            let value = e.target.value.replace(/[^a-zA-Z0-9_À-ÿ]/g, '_').toLowerCase();
            let unique = true;
            do {
                unique = tools.filter((t) => t.tool_id === value).length === 0;

                if (unique) {
                    setToolId(value);
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
            modalHeading={(mode == "create" ? "Create a new tool" : "Update tool " + tool.tool_id)}
            modalLabel="Tools"
            primaryButtonText={(mode == "create" ? "Add" : "Update")}
            secondaryButtonText="Cancel"
            preventCloseOnClickOutside
            shouldSubmitOnEnter
            onRequestSubmit={onRequestSubmit}>
            <p style={{ marginBottom: '1rem' }}>
                {(mode == "create" ? "Add a new tool to your Owl Agent framework." : "Update the tool information.")}
            </p>
            <Tools style={{ width: '5rem', height: 'auto', padding: "0.5rem" }} />

            <TextInput data-modal-primary-focus id="text-input-tool-name"
                labelText="Tool Name"
                placeholder="e.g. Get Contract by Number."
                invalid={empty}
                invalidText="This field cannot be empty"
                value={toolName}
                onChange={checkAndBuildId} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextInput id="text-input-2"
                labelText="Description"
                placeholder="e.g. this tool is to be attached to an agent based on LLM Mixtral to discover client's contracts."
                value={toolDescription}
                onChange={(e) => setToolDescription(e.target.value)} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextInput id="text-input-3"
                labelText="Class Name"
                placeholder="class name of the tool"
                value={toolClassName}
                onChange={(e) => setToolClassName(e.target.value)} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextInput id="text-input-4"
                labelText="Function Name"
                placeholder="function name of the tool"
                value={toolFctName}
                onChange={(e) => setToolFctName(e.target.value)} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextInput id="text-input-5"
                labelText="Argument Schema Class"
                placeholder="argument schema class of the tool"
                value={toolArgSchemaClass}
                onChange={(e) => setToolArgSchemaClass(e.target.value)} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

        </Modal>
    )
};

export default Tool;
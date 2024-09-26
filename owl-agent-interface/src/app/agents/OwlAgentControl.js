import { Button, Column, ExpandableTile, Grid, TextArea, TileAboveTheFoldContent, TileBelowTheFoldContent, Toggle } from "@carbon/react";
import React, { useEffect, useState } from "react";
import { useTranslation } from 'react-i18next';
import AgentModel from "./AgentModel";
import AgentTools from "./AgentTools";
import UploadDocument from "../documents/UploadDocument";
import { Save } from "@carbon/react/icons";

const OwlAgentControl = ({ backendBaseAPI, activeAgent, setActiveAgent, promptEnglishContent, useFileSearch, setUseFileSearch, setError }) => {
    const [agentModelName, setAgentModelName] = useState("gpt-4o");
    const [agentModelClassName, setAgentModelClassName] = useState("langchain_openai.ChatOpenAI");
    const [promptContent, setPromptContent] = useState("");
    const [toolSelectedItems, setToolSelectedItems] = useState({ selectedItems: [] });

    const { t, i18n } = useTranslation();

    useEffect(() => {
        if (activeAgent) {
            setAgentModelName(activeAgent.modelName);
            setAgentModelClassName(activeAgent.modelClassName);
            setPromptContent(promptEnglishContent);
            setToolSelectedItems({ selectedItems: [...activeAgent.tools] });
        }
    }, [activeAgent]);

    const saveActiveAgent = async () => {
        const agent = {
            modelName: agentModelName,
            modelClassName: agentModelClassName,
            tools: toolSelectedItems.selectedItems,
        };

        try {
            const response = await fetch(`${backendBaseAPI}a/agents/${activeAgent.agentId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(agent),
            });

            if (response.ok) {
                console.log('Agent updated successfully');
                setActiveAgent(agent);
            } else {
                console.error('Agent update failed', response.statusText);
                setError('Agent update failed: ' + response.statusText);
            }
        } catch (error) {
            console.error('Error updating agent:', error);
            setError('Error updating agent:' + error.message);
        }
    }

    return (
        <div className="owl-agent-control">
            <ExpandableTile id="owl-agent-control" tileCollapsedIconText="Expand settings" tileExpandedIconText="Collapse settings">
                <TileAboveTheFoldContent>
                    <div>Agent settings</div>
                </TileAboveTheFoldContent>
                <TileBelowTheFoldContent>
                    <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

                    <Grid>
                        <Column sm={2} md={4} lg={8}>
                            <AgentModel agentModelClassName={agentModelClassName} setAgentModelClassName={setAgentModelClassName} agentModelName={agentModelName} setAgentModelName={setAgentModelName} />

                            <TextArea id="text-area-prompt-content"
                                labelText="Prompt content (English)"
                                value={promptContent}
                                onChange={(e) => setPromptContent(e.target.value)}
                                placeholder="e.g. You are a customer service manager with expertise in resolving complex financial disputes..." />
                            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
                        </Column>
                        <Column sm={2} md={4} lg={8}>
                            <AgentTools backendBaseAPI={backendBaseAPI} toolSelectedItems={toolSelectedItems} setToolSelectedItems={setToolSelectedItems} setError={setError} />

                            <Toggle id="toggle-use-document-search"
                                labelText="Use document search"
                                defaultToggled={true}
                                labelB="Yes"
                                onClick={() => setUseFileSearch(!useFileSearch)} />
                            {useFileSearch && <UploadDocument backendBaseAPI={backendBaseAPI} setError={setError} />}
                        </Column>
                        <Column sm={4} md={8} lg={16}>
                            <div style={{ display: 'flex', alignItems: 'flex-end', marginTop: '1rem' }}>
                                <Button renderIcon={Save} kind="primary" onClick={saveActiveAgent}>{"Apply changes"}</Button>
                            </div>
                        </Column>
                    </Grid>
                </TileBelowTheFoldContent>
            </ExpandableTile>
        </div>
    );
};

export default OwlAgentControl;
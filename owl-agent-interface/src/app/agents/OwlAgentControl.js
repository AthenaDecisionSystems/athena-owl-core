import { Column, ExpandableTile, Grid, TextArea, TileAboveTheFoldContent, TileBelowTheFoldContent, Toggle } from "@carbon/react";
import React, { useState } from "react";
import { useTranslation } from 'react-i18next';
import AgentModel from "./AgentModel";
import AgentTools from "./AgentTools";
import UploadDocument from "../documents/UploadDocument";

const OwlAgentControl = ({ backendBaseAPI, useFileSearch, setUseFileSearch, setError }) => {
    const [agentModelName, setAgentModelName] = useState("gpt-4o");
    const [agentModelClassName, setAgentModelClassName] = useState("langchain_openai.ChatOpenAI");
    const [promptContent, setPromptContent] = useState("");
    const [toolSelectedItems, setToolSelectedItems] = useState({ selectedItems: [] });

    const { t, i18n } = useTranslation();

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
                    </Grid>
                </TileBelowTheFoldContent>
            </ExpandableTile>
        </div>
    );
};

export default OwlAgentControl;
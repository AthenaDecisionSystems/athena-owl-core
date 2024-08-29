// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import "./Agent.css";
import React, { useEffect, useState, forwardRef, useImperativeHandle } from 'react';
import Attachments from './Attachments';
import { useDispatch, useSelector } from 'react-redux';
import { setError } from './reducer/error.action';
import Switch from './Switch'
import { useTranslation } from 'react-i18next';

const Agent = forwardRef(({ agentId, informUser, changeUseODMStatus, changeUseFileSearchStatus }, ref) => {
    const [promptRef, setPromptRef] = useState("")
    const [instructions, setInstructions] = useState("")
    const [defaultInstructions, setDefaultInstructions] = useState("")

    const [useODM, setUseODM] = useState(false)
    const [useFileSearch, setUseFileSearch] = useState(true)
    const [dirty, setDirty] = useState(false)

    const serverUrl = useSelector((state) => state.serverUrlReducer.serverUrl)
    const dispatch = useDispatch()

    const { t, i18n } = useTranslation();
    const language = i18n.language;

    useEffect(() => {
        const fetchPromptRefAndGetPrompt = async () => {
            fetch(serverUrl + "a/agents/" + agentId)
                .then(response => response.json())
                .then(data => {
                    console.log("Prompt ref: " + data.prompt_ref);
                    getPrompt(data.prompt_ref, language);
                    setPromptRef(data.prompt_ref);
                })
                .catch(error => {
                    console.error('Error:', error)
                })
        };

        if (agentId && agentId !== "") {
            fetchPromptRefAndGetPrompt();
        }
    }, [agentId]); // eslint-disable-line

    useEffect(() => {
        setInstructions(defaultInstructions);
    }, [defaultInstructions]);

    useEffect(() => {
        changeUseODMStatus(useODM);
        informUser(useODM ? t("agent.msg.agentConfiguredToUseODM") : t("agent.msg.agentConfiguredNotToUseODM"))
    }, [useODM]); // eslint-disable-line

    useEffect(() => {
        changeUseFileSearchStatus(useFileSearch);
    }, [useFileSearch]); // eslint-disable-line

    const getPrompt = async (prompt, language) => {
        fetch(serverUrl + "a/prompts/" + prompt + "/" + language)
            .then(response => response.json())
            .then(data => {
                let str = JSON.stringify(data);
                // Remove quotes if present
                if (str.startsWith("\"") && str.endsWith("\"")) {
                    str = str.slice(1, -1);
                }
                // Change \n with new line
                str = str.replace(/\\n/g, "\n");
                // Change \" with "
                str = str.replace(/\\"/g, "\"");
                // Delete leading and trailing spaces
                str = str.trim();
                setInstructions(str);
                if (defaultInstructions === "") {
                    setDefaultInstructions(str);
                }
            })
            .catch(error => {
                console.error('Error:', error)
                dispatch(setError(error))
            });
    }

    useImperativeHandle(ref, () => ({
        localizeAgent: (lang) => {
            getPrompt(promptRef, lang)
            informUser(t("app.msg.welcome"))
            setDirty(false)
        },
        updatePrompt: () => {
            getPrompt(promptRef, language)
            informUser("Prompt updated.")
            setDirty(false)
        }
    }));

    const dirtyFlag = () => {
        setDirty(instructions !== defaultInstructions)
    }

    const reinitDefaultValues = () => {
        setInstructions(defaultInstructions);
        setDirty(false);
    }

    const updateAgent = async () => {
        const inst = instructions.trim();
        if (inst === defaultInstructions) {
            informUser("No change.")
            setInstructions(defaultInstructions);
            setDirty(false);
            return
        }
        if (inst === "") {
            informUser("Instructions can't be empty");
            setInstructions(defaultInstructions);
            setDirty(false);
            return
        }

        const body = {
            "prompt_key": promptRef,
            "prompt_locale": language,
            "prompt_content": instructions
        }

        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
            body: JSON.stringify(body)
        };

        fetch(serverUrl + "a/prompts/", requestOptions)
            .then(response => {
                if (response.status === 200) {
                    setDirty(false);
                    setDefaultInstructions(instructions);
                } else {
                    console.error('Error:', response)
                }
            })
            .catch(error => {
                console.error('Error:', error)
                dispatch(setError(error))
            });
    }

    const reinitConversation = () => {
        informUser("---Restart conversation---");
    }

    return (
        <div className="agent">
            <div className="agent-title">{t("agent.lbl.title")}</div>
            <div className="agent-label">{t("agent.lbl.instructions")}</div>
            <div className="agent-input-zone">
                <textarea name="instructions" rows="15" value={instructions}
                    onChange={(e) => { setInstructions(e.target.value) }}
                    onKeyUp={(e) => { setInstructions(e.target.value); dirtyFlag() }}></textarea>
            </div>

            <div className="agent-input-zone">
                {dirty && <div className="agent-button-block">
                    <div className="agent-button agent-button-in-block" onClick={reinitDefaultValues}>{t("agent.btn.reinitDefaultValues")}</div>
                    <div className="agent-button agent-button-in-block" onClick={updateAgent}>{t("agent.btn.updateAgent")}</div>
                </div>}
            </div>

            <div className="agent-input-zone">
                <div className="agent-one-line">
                    <div className="agent-label">{t("agent.chk.useFileSearch")}</div>
                    <Switch value={useFileSearch} onClick={setUseFileSearch} />
                </div>
                <div className={useFileSearch ? "agent-object-visible" : "agent-object-hidden"}>
                    <Attachments informUser={informUser} />
                </div>
            </div>

            <div className="agent-label-block">
                <div className="agent-one-line">
                    <div className="agent-label">{t("agent.chk.useBusinessRules")}</div>
                    <Switch value={useODM} onClick={setUseODM} />
                </div>
            </div>
            <hr className="agent-space-around" />
            <div className="agent-button-block">
                <div className="agent-small-button " onClick={reinitConversation}>{t("agent.btn.reinitConversation")}</div>
            </div>
        </div>
    );
});

export default Agent;
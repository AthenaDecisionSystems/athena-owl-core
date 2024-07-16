// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import "./Assistant.css";
import React, { useEffect, useState, forwardRef, useImperativeHandle } from 'react';
import Attachments from './Attachments';
import { useDispatch, useSelector } from 'react-redux';
import { setError } from './reducer/error.action';
import Switch from './Switch'
import { useTranslation } from 'react-i18next';

const Assistant = forwardRef(({ assistantId, informUser, changeUseODMStatus, changeUseFileSearchStatus }, ref) => {
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
            fetch(serverUrl + "a/assistants/" + assistantId)
                .then(response => response.json())
                .then(data => {
                    console.log("Agent id: " + data.agent_id, data);
                    fetch(serverUrl + "a/agents/" + data.agents[0])
                        .then(response => response.json())
                        .then(data => {
                            console.log("Prompt ref: " + data.prompt_ref);
                            getPrompt(data.prompt_ref, language);
                            setPromptRef(data.prompt_ref);
                        })
                        .catch(error => {
                            console.error('Error:', error)
                        })
                })
                .catch(error => {
                    console.error('Error:', error)
                });
        }

        if (assistantId && assistantId !== "") {
            fetchPromptRefAndGetPrompt();
        }
    }, [assistantId]); // eslint-disable-line

    useEffect(() => {
        setInstructions(defaultInstructions);
    }, [defaultInstructions]);

    useEffect(() => {
        changeUseODMStatus(useODM);
        informUser(useODM ? t("assistant.msg.agentConfiguredToUseODM") : t("assistant.msg.agentConfiguredNotToUseODM"))
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
        localizeAssistant: (lang) => {
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

    const updateAssistant = async () => {
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
        <div className="assistant">
            <div className="assistant-title">{t("assistant.lbl.title")}</div>
            <div className="assistant-label">{t("assistant.lbl.instructions")}</div>
            <div className="assistant-input-zone">
                <textarea name="instructions" rows="15" value={instructions}
                    onChange={(e) => { setInstructions(e.target.value) }}
                    onKeyUp={(e) => { setInstructions(e.target.value); dirtyFlag() }}></textarea>
            </div>

            <div className="assistant-input-zone">
                {dirty && <div className="assistant-button-block">
                    <div className="assistant-button assistant-button-in-block" onClick={reinitDefaultValues}>{t("assistant.btn.reinitDefaultValues")}</div>
                    <div className="assistant-button assistant-button-in-block" onClick={updateAssistant}>{t("assistant.btn.updateAssistant")}</div>
                </div>}
            </div>

            <div className="assistant-input-zone">
                <div className="assistant-one-line">
                    <div className="assistant-label">{t("assistant.chk.useFileSearch")}</div>
                    < Switch value={useFileSearch} onClick={setUseFileSearch} />
                </div>
                <div className={useFileSearch ? "assistant-object-visible" : "assistant-object-hidden"}>
                    <Attachments informUser={informUser} />
                </div>
            </div>

            <div className="assistant-label-block">
                <div className="assistant-one-line">
                    <div className="assistant-label">{t("assistant.chk.useBusinessRules")}</div>
                    <Switch value={useODM} onClick={setUseODM} />
                </div>
            </div>
            <hr className="assistant-space-around" />
            <div className="assistant-button-block">
                <div className="assistant-small-button " onClick={reinitConversation}>{t("assistant.btn.reinitConversation")}</div>
            </div>
        </div>
    );
});

export default Assistant;
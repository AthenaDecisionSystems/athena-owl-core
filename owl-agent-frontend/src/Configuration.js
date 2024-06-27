// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import "./Configuration.css";
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setServerUrl } from "./reducer/server_url.action";
import { setLanguage } from "./reducer/language.action";
import { useTranslation } from 'react-i18next';

const Configuration = ({ onDismiss, assistantId, assistantIdWithoutRules, onChangeLanguage, setAssistantId, setAssistantIdWithoutRules }) => {
    const serverUrl = useSelector((state) => state.serverUrlReducer.serverUrl)
    const defaultServerUrl = serverUrl

    // The following state is used to detect a change so the "Set" button is displayed
    const [serverUrlNewValue, setServerUrlNewValue] = useState(defaultServerUrl)
    const [assistantList, setAssistantList] = useState([])

    const dispatch = useDispatch()

    const { t, i18n } = useTranslation();
    const language = i18n.language;

    useEffect(() => {
        const getAssistantList = async () => {
            fetch(serverUrl + "a/assistants")
                .then(response => response.json())
                .then(data => {
                    let list = data.map((assistant) => {
                        return assistant.assistant_id;
                    });
                    setAssistantList(list);
                })
                .catch(error => {
                    console.error('Error:', error)
                });
        }
        getAssistantList();
    }, []); // eslint-disable-line

    const handleClickServerUrl = async () => {
        dispatch(setServerUrl(serverUrlNewValue));
    }

    const handleChangeLanguage = async (e) => {
        const language = e.target.value;
        i18n.changeLanguage(language);
        dispatch(setLanguage(language));
        onChangeLanguage();
    }

    return (
        <div className="configuration-panel">
            <div className="configuration-panel-close" onClick={onDismiss}>X</div>

            <div className="assistant-label">{t("configuration.lbl.language")}</div>
            <div className="assistant-input-zone">
                <select name="language" value={language} onChange={handleChangeLanguage}>
                    <option value="en">🇬🇧 English</option>
                    <option value="es">🇪🇸 Español</option>
                    <option value="fr">🇫🇷 Français</option>
                </select>
            </div>

            <div className="assistant-label">{t("configuration.lbl.serverURL")}</div>
            <div className="configuration-url">
                <input type="text" name="serverUrl"
                    placeholder={serverUrl}
                    value={serverUrlNewValue}
                    onChange={(e) => setServerUrlNewValue(e.target.value)} />
                {serverUrlNewValue !== serverUrl &&
                    <div className="configuration-url-set" onClick={handleClickServerUrl}>Set</div>}
            </div>

            <div className="assistant-label">Assistant Id with Rules</div>
            <div className="assistant-input-zone">
                <select name="assistantId" value={assistantId} onChange={(e) => { setAssistantId(e.target.value) }}>
                    {assistantList.map((assistantId) => {
                        return <option key={assistantId} value={assistantId}>{assistantId}</option>
                    })}
                </select>
            </div>

            <div className="assistant-label">Assistant Id without Rules</div>
            <div className="assistant-input-zone">
                <select name="assistantIdWithoutRules" value={assistantIdWithoutRules} onChange={(e) => { setAssistantIdWithoutRules(e.target.value) }}>
                    {assistantList.map((assistantId) => {
                        return <option key={assistantId} value={assistantId}>{assistantId}</option>
                    })}
                </select>
            </div>
        </div>
    );
};

export default Configuration;
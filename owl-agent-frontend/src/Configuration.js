// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import "./Configuration.css";
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setServerUrl } from "./reducer/server_url.action";
import { setLanguage } from "./reducer/language.action";
import { useTranslation } from 'react-i18next';

const Configuration = ({ onDismiss, agentId, agentIdWithoutRules, onChangeLanguage, setAgentId, setAgentIdWithoutRules }) => {
    const serverUrl = useSelector((state) => state.serverUrlReducer.serverUrl)
    const defaultServerUrl = serverUrl

    // The following state is used to detect a change so the "Set" button is displayed
    const [serverUrlNewValue, setServerUrlNewValue] = useState(defaultServerUrl)
    const [agentList, setAgentList] = useState([])

    const dispatch = useDispatch()

    const { t, i18n } = useTranslation();
    const language = i18n.language;

    useEffect(() => {
        const getAgentList = async () => {
            fetch(serverUrl + "a/agents")
                .then(response => response.json())
                .then(data => {
                    let list = data.map((agent) => {
                        return agent.agent_id;
                    });
                    setAgentList(list);
                })
                .catch(error => {
                    console.error('Error:', error)
                });
        }
        getAgentList();
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

            <div className="agent-label">{t("configuration.lbl.language")}</div>
            <div className="agent-input-zone">
                <select name="language" value={language} onChange={handleChangeLanguage}>
                    <option value="en">🇬🇧 English</option>
                    <option value="es">🇪🇸 Español</option>
                    <option value="fr">🇫🇷 Français</option>
                </select>
            </div>

            <div className="agent-label">{t("configuration.lbl.serverURL")}</div>
            <div className="configuration-url">
                <input type="text" name="serverUrl"
                    placeholder={serverUrl}
                    value={serverUrlNewValue}
                    onChange={(e) => setServerUrlNewValue(e.target.value)} />
                {serverUrlNewValue !== serverUrl &&
                    <div className="configuration-url-set" onClick={handleClickServerUrl}>Set</div>}
            </div>

            <div className="agent-label">Agent Id with Rules</div>
            <div className="agent-input-zone">
                <select name="agentId" value={agentId} onChange={(e) => { setAgentId(e.target.value) }}>
                    {agentList.map((agentId) => {
                        return <option key={agentId} value={agentId}>{agentId}</option>
                    })}
                </select>
            </div>

            <div className="agent-label">Agent Id without Rules</div>
            <div className="agent-input-zone">
                <select name="agentIdWithoutRules" value={agentIdWithoutRules} onChange={(e) => { setAgentIdWithoutRules(e.target.value) }}>
                    {agentList.map((agentId) => {
                        return <option key={agentId} value={agentId}>{agentId}</option>
                    })}
                </select>
            </div>
        </div>
    );
};

export default Configuration;
// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import "./Configuration.css";
import "./Slider.css";
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setServerUrl } from "./reducer/server_url.action";
import { setLanguage } from "./reducer/language.action";
import { useTranslation } from 'react-i18next';

const Configuration = ({ onDismiss, onChangeLanguage, onChangeModelParameters }) => {
    const serverUrl = useSelector((state) => state.serverUrlReducer.serverUrl)
    const defaultServerUrl = serverUrl

    // The following state is used to detect a change so the "Set" button is displayed
    const [serverUrlNewValue, setServerUrlNewValue] = useState(defaultServerUrl)

    const [modelParameters, setModelParameters] = useState({
        "modelName": "gpt-4o",
        "modelClass": "agent_openai",
        "temperature": 0,
        "top_k": 1,
        "top_p": 1
    });

    const [sliderValue, setSliderValue] = useState(modelParameters.temperature);

    const dispatch = useDispatch()

    const { t, i18n } = useTranslation();
    const language = i18n.language;


    const handleClickServerUrl = async () => {
        dispatch(setServerUrl(serverUrlNewValue));
    }

    const handleChangeLanguage = async (e) => {
        const language = e.target.value;
        i18n.changeLanguage(language);
        dispatch(setLanguage(language));
        onChangeLanguage();
    }

    const changeTemperatureValue = (value) => {
        let mp = {
            "modelName": modelParameters.modelName,
            "modelClass": modelParameters.modelClass,
            "temperature": value,
            "top_k": modelParameters.top_k,
            "top_p": modelParameters.top_p
        }
        setModelParameters(mp);
        onChangeModelParameters(mp);
    }
    const setModel = (value) => {
        let mp = {
            "modelName": value,
            "modelClass": modelParameters.modelClass,
            "temperature": modelParameters.temperature,
            "top_k": modelParameters.top_k,
            "top_p": modelParameters.top_p
        }
        setModelParameters(mp);
        onChangeModelParameters(mp);
    }

    const getBackgroundSize = () => {
        return { backgroundSize: `${sliderValue}% 100%` };
    };

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

            <div className="assistant-label">{t("configuration.lbl.model")}</div>
            <div className="assistant-input-zone">
                <select name="model" value={modelParameters.modelName} onChange={(e) => { setModel(e.target.value) }}>
                    <option value="ibm/granite-13b-instruct-v2">Watsonx/granite-20b-multilingual</option>
                    <option value="ibm/llama-3-8b-instruct">Watsonx/llama-3-8b-instruct</option>
                    <option value="ibm/mixtral-8x7b-instruct">Watsonx/mixtral-8x7b-instruct</option>
                    <option value="gpt-4o">gpt-4o</option>
                    <option value="gpt-4-turbo">gpt-4-turbo</option>
                    <option value="gpt-3.5-turbo-16k">gpt-3.5-turbo-16k</option>
                </select>
            </div>

            <div className="assistant-one-line">
                <div className="assistant-label">{t("configuration.lbl.temperature")}</div>
                <div>
                    {sliderValue / 100}
                    &nbsp;
                    <input
                        type="range"
                        min="0"
                        max="100"
                        onChange={(e) => setSliderValue(e.target.value)}
                        onMouseUp={(e) => changeTemperatureValue(e.target.value)}
                        style={getBackgroundSize()}
                        value={sliderValue}
                    />
                </div>
            </div>
        </div>
    );
};

export default Configuration;
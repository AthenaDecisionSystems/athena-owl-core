import { Modal, TextArea, TextInput } from '@carbon/react';
import React, { useEffect, useRef, useState } from 'react';
import { AiGovernancePrompt } from '@carbon/pictograms-react';
import { Octokit } from '@octokit/core';

const octokitClient = new Octokit({});

const locales = ["en", "fr", "es"];

const Prompt = ({ backendBaseAPI, mode, prompt, prompts, openState, setOpenState, onSuccess, setError }) => {
    // mode = 'create' or 'edit'
    const [empty, setEmpty] = useState(false);
    const [promptId, setPromptId] = useState("");
    const [promptName, setPromptName] = useState("");
    const [promptContent, setPromptContent] = useState({ en: "", fr: "", es: "" })
    const [modeLocales, setModeLocales] = useState({ en: "create", fr: "create", es: "create" });

    const ref = useRef(null);

    useEffect(() => {
        if (mode === 'edit') {
            setPromptId(prompt.prompt_id);
            setPromptName(prompt.name);

            let content = {};
            let modes = {};
            locales.forEach(locale => {
                const promptLocale = prompt.locales.find(p => p.locale === locale);
                content[locale] = promptLocale ? promptLocale.text : "";
                modes[locale] = promptLocale ? "edit" : "create";

            })
            setPromptContent(content);
            setModeLocales(modes);
        }
        setEmpty(false)
    }, [prompt]);

    const upsertPrompt = async (mode, locale) => {
        let ed = (mode === "create" ? "created" : "updated");
        let ing = (mode === "create" ? "creating" : "updating");

        try {
            const res = await octokitClient.request(
                (mode === "create" ? "POST " : "PUT ") + backendBaseAPI + "a/prompts/", {
                "prompt_key": promptId, // should be prompt_id
                "name": promptName, // not saved
                "prompt_locale": locale,
                "prompt_content": promptContent[locale]
            });

            if (res.status === 200) {
                console.log(`Prompt ${ed}`, res.data);
                onSuccess();
            } else {
                setError(`Error ${ing} prompt (` + res.status + ')');
                console.error(`Error ${ing} prompt`, res);
            }
        }
        catch (error) {
            setError(`Error ${ing} prompt: ` + error.message);
            console.error(`Error ${ing} prompt`, error);
        }
    }

    const onRequestSubmit = () => {
        if (!promptName) {
            setEmpty(true);
        } else {
            const nonEmptyPrompts = Object.keys(promptContent).filter(locale => promptContent[locale] && promptContent[locale].trim().length > 0);
            if (mode === "create") {
                if (nonEmptyPrompts.length === 0) {
                    // Create prompt with empty English content
                    upsertPrompt(mode, "en");
                } else {
                    // Create prompt with first non-empty content and iterate over the rest in edit mode
                    upsertPrompt(mode, nonEmptyPrompts[0]);
                    for (let i = 1; i < nonEmptyPrompts.length; i++) {
                        upsertPrompt("edit", nonEmptyPrompts[i]);
                    }
                }
            } else {
                console.log(nonEmptyPrompts)
                nonEmptyPrompts.forEach(locale => {
                    upsertPrompt(modeLocales[locale], locale);
                });
            }

            setPromptId("");
            setPromptContent({ en: "", fr: "", es: "" });
            setModeLocales({ en: "create", fr: "create", es: "create" });

            setOpenState(false);
        }
    }

    const checkAndBuildId = (e) => {
        setEmpty(!e.target.value);
        setPromptName(e.target.value);
        if (mode === "create") {
            let value = e.target.value.replace(/[^a-zA-Z0-9_À-ÿ]/g, '_').toLowerCase();
            let unique = true;
            do {
                unique = prompts.filter((t) => t.prompt_id === value).length === 0;

                if (unique) {
                    setPromptId(value);
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
            modalHeading={(mode == "create" ? "Create a new prompt" : "Update prompt " + promptId)}
            modalLabel="Prompts"
            primaryButtonText={(mode == "create" ? "Add" : "Update")}
            secondaryButtonText="Cancel"
            preventCloseOnClickOutside
            shouldSubmitOnEnter
            onRequestSubmit={onRequestSubmit}>
            <p style={{ marginBottom: '1rem' }}>
                {(mode == "create" ? "Add a new prompt to your Owl Agent framework." : "Update the prompt information.")}
            </p>
            <AiGovernancePrompt style={{ width: '5rem', height: 'auto', padding: "0.5rem" }} />

            <TextInput data-modal-primary-focus id="text-input-1"
                labelText="Prompt name"
                placeholder="e.g. Analyze email from client and make a decision about..."
                invalid={empty}
                invalidText="This field cannot be empty"
                value={promptName}
                onChange={checkAndBuildId} />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextArea id="text-area-1"
                labelText="Prompt content (English)"
                value={promptContent.en}
                onChange={(e) => setPromptContent({ en: e.target.value, fr: promptContent.fr, es: promptContent.es })}
                placeholder="e.g. This is the prompt used by Mixtral in combination with tools and Business Rules to make intelligent decisions..." />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextArea id="text-area2"
                labelText="Prompt content (French)"
                value={promptContent.fr}
                onChange={(e) => setPromptContent({ en: promptContent.en, fr: e.target.value, es: promptContent.es })}
                placeholder="e.g. Il s'agit du prompt utilisé par Mixtral en combinaison avec des outils et des règles métier pour prendre des décisions intelligentes...." />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <TextArea id="text-area-3"
                labelText="Prompt content (Spanish)"
                value={promptContent.es}
                onChange={(e) => setPromptContent({ en: promptContent.en, fr: promptContent.fr, es: e.target.value })}
                placeholder="e.g. Este es el prompt utilizado por Mixtral en combinación con herramientas y Reglas de Negocio para tomar decisiones inteligentes..." />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
        </Modal>
    )
};

export default Prompt;
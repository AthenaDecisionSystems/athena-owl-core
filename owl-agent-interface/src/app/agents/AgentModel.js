import { Select, SelectItem } from "@carbon/react";
import React from "react";

const AgentModel = ({ agentModelClassName, setAgentModelClassName, agentModelName, setAgentModelName }) => {

    const modelClassNames = [
        { name: "Anthropic", value: "langchain_anthropic.ChatAnthropic", modelNames: ["claude-3-opus-20240229"] },
        { name: "Mistral AI", value: "langchain_mistralai.chat_models.ChatMistralAI", modelNames: ["mistral-large-latest", "open-mixtral-8x7b",] },
        {
            name: "Open AI", value: "langchain_openai.ChatOpenAI", modelNames: ["gpt-4o-2024-08-06", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
        },
    ];

    const changeModelClassName = (e) => {
        setAgentModelClassName(e.target.value);
        setAgentModelName(modelClassNames.find((modelClassName) => (modelClassName.value === e.target.value)).modelNames[0]);
    }

    return (
        <div>
            {agentModelClassName && <Select id="select-model-class-name"
                value={agentModelClassName}
                labelText="LLM"
                onChange={(e) => changeModelClassName(e)}>
                {modelClassNames.map((modelClassName, i) => (<SelectItem key={i} value={modelClassName.value} text={modelClassName.name} />))}
            </Select>}
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            {agentModelName && <Select id="select-model-name"
                value={agentModelName}
                labelText="Model Name"
                onChange={(e) => setAgentModelName(e.target.value)}>
                {modelClassNames.find((modelClassName) => (modelClassName.value === agentModelClassName)).modelNames.map((modelName, i) => (<SelectItem key={i} value={modelName} text={modelName} />))}
            </Select>}
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
        </div>
    );
};

export default AgentModel;
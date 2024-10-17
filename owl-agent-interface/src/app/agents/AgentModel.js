import { Select, SelectItem } from "@carbon/react";
import React from "react";

const AgentModel = ({ agentModelClassName, setAgentModelClassName, agentModelName, setAgentModelName }) => {

    const modelClassNames = [
        { name: "Anthropic", value: "langchain_anthropic.ChatAnthropic", modelNames: ["claude-3-opus-20240229"] },
        { name: "Mistral AI", value: "langchain_mistralai.chat_models.ChatMistralAI", modelNames: ["mistral-large-latest", "open-mixtral-8x7b",] },
        { name: "Open AI", value: "langchain_openai.ChatOpenAI", modelNames: ["gpt-4o-2024-08-06", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"] },
        { name: "Watsonx LLM", value: "langchain_ibm.WatsonxLLM", modelNames: ['google/flan-t5-xl', 'google/flan-t5-xxl', 'google/flan-ul2', 'ibm/granite-13b-chat-v2', 'ibm/granite-13b-instruct-v2', 'ibm/granite-20b-multilingual', 'ibm/granite-7b-lab', 'meta-llama/llama-2-13b-chat', 'meta-llama/llama-3-1-70b-instruct', 'meta-llama/llama-3-1-8b-instruct', 'meta-llama/llama-3-70b-instruct', 'meta-llama/llama-3-8b-instruct', 'mistralai/mistral-large', 'mistralai/mixtral-8x7b-instruct-v01'] },
        { name: "Chat Watsonx", value: "langchain_ibm.ChatWatsonx", modelNames: ['mistralai/mistral-large'] },
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
                {modelClassNames.find((modelClassName) => (modelClassName.value === agentModelClassName))?.modelNames.map((modelName, i) => (<SelectItem key={i} value={modelName} text={modelName} />))}
            </Select>}
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
        </div>
    );
};

export default AgentModel;
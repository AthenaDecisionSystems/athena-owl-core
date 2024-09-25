import { Select, SelectItem } from "@carbon/react";
import React from "react";

const AgentModel = ({ agentModelClassName, setAgentModelClassName, agentModelName, setAgentModelName }) => {

    const modelClassNames = [
        { name: "Anthropic", value: "langchain_anthropic.ChatAnthropic", modelNames: ["claude-3-opus-20240229"] },
        { name: "Mistral AI", value: "langchain_mistralai.chat_models.ChatMistralAI", modelNames: ["open-mixtral-8x7b", "mistral-large-latest"] },
        { name: "Ollama", value: "langchain_community.chat_models.ChatOllama", modelNames: [] },
        { name: "Open AI", value: "langchain_openai.ChatOpenAI", modelNames: ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"] },
    ];

    return (
        <div>
            <Select id="select-model-class-name"
                value={agentModelClassName}
                labelText="Model Class Name"
                onChange={(e) => setAgentModelClassName(e.target.value)}>
                <SelectItem value="" text="" />
                {modelClassNames.map((modelClassName, i) => (<SelectItem key={i} value={modelClassName.value} text={modelClassName.name} />))}
            </Select>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <Select id="select-model-name"
                value={agentModelName}
                labelText="Model Name"
                onChange={(e) => setAgentModelName(e.target.value)}>
                <SelectItem value="" text="" />
                {modelClassNames.find((modelClassName) => (modelClassName.value === agentModelClassName)).modelNames.map((modelName, i) => (<SelectItem key={i} value={modelName} text={modelName} />))}
            </Select>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
        </div>
    );
};

export default AgentModel;
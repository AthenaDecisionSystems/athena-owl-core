import { Select, SelectItem } from "@carbon/react";
import React from "react";

const AgentModel = ({ modelClassNames, agentModelClassName, setAgentModelClassName, agentModelName, setAgentModelName, setError }) => {

    const changeModelClassName = (e) => {
        setAgentModelClassName(e.target.value);
        setAgentModelName(modelClassNames.find((modelClassName) => (modelClassName.value === e.target.value)).modelNames[0]);
    }

    return (
        <div>
            <Select id="select-model-class-name"
                value={agentModelClassName}
                labelText="LLM"
                onChange={(e) => changeModelClassName(e)}>
                {modelClassNames.map((modelClassName, i) => (<SelectItem key={i} value={modelClassName.value} text={modelClassName.name} />))}
            </Select>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />

            <Select id="select-model-name"
                value={agentModelName}
                labelText="Model Name"
                onChange={(e) => setAgentModelName(e.target.value)}>
                {modelClassNames.find((modelClassName) => (modelClassName.value === agentModelClassName))?.modelNames.map((modelName, i) => (<SelectItem key={i} value={modelName} text={modelName} />))}
            </Select>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '1rem' }} />
        </div>
    );
};

export default AgentModel;
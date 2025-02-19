import React, { useEffect, useState } from 'react';
import { Button, Modal } from '@carbon/react';
import { QuestionAndAnswer } from '@carbon/pictograms-react';
import OwlAgent from './OwlAgent';

// --- OwlAgentModal ---
const OwlAgentModal = ({ backendBaseAPI, agent, promptEnglishContent, openState, setOpenState, randomNumber, setError }) => {
    const [activeAgent, setActiveAgent] = useState(null);
    const [useFileSearch, setUseFileSearch] = useState(false);
    const [useDecisionServices, setUseDecisionServices] = useState(false);

    useEffect(() => {
        setActiveAgent(agent);
    }, [agent]);

    return (
        <Modal open={openState}
            onRequestClose={() => setOpenState(false)}
            modalHeading={activeAgent && (activeAgent.name ? activeAgent.name : activeAgent.agent_id)}
            passiveModal
            size='lg'
            preventCloseOnClickOutside
            hasScrollingContent
            className="owl-agent-modal">

            <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start" }}>
                <QuestionAndAnswer style={{ width: '5rem', height: 'auto', padding: "0.5rem" }} />
            </div>

            <OwlAgent backendBaseAPI={backendBaseAPI} agent={agent} promptEnglishContent={promptEnglishContent} useFileSearch={useFileSearch} useDecisionServices={useDecisionServices} openState={openState} randomNumber={randomNumber} setError={setError} />
        </Modal >
    );
};

export default OwlAgentModal;
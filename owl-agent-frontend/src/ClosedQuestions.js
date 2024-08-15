import './ClosedQuestions.css';

import React, { useRef } from 'react';
import { useTranslation } from 'react-i18next';
import ClosedQuestion from './ClosedQuestion';

const ClosedQuestions = ({ lastMessage, questions, feedback }) => {
    const questionRefs = useRef([]);

    const { t } = useTranslation();

    const validateClosedAnswers = () => {
        let answers = new Array(questions.length).fill(null);
        let allAnswered = true;
        questionRefs.current.forEach(ref => {
            if (ref) {
                let answer = ref.getFullAnswer();
                if (answer.input === null) {
                    allAnswered = false;
                }
                answers[answer.index] = { key_name: answer.key_name, input: answer.input };
            }
        });
        if (allAnswered) {
            feedback(answers);
        }
    }

    // Closed questions are answerable only if they have been received by the last message
    return (
        <div>
            {questions.map((question, i) =>
                <div>
                    <ClosedQuestion
                        ref={el => questionRefs.current[i] = el}
                        index={i}
                        question={question}
                        disabled={!lastMessage} />
                    <br />
                </div>)}
            {lastMessage && (<hr style={{ marginBottom: "1rem" }} />)}
            {lastMessage && (<button className="closed-questions-button" onClick={validateClosedAnswers}> {t("app.btn.send")}</button>)}
        </div>
    );
};

export default ClosedQuestions;
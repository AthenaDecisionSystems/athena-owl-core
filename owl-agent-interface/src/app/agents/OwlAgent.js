import React, { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Modal, TextArea } from '@carbon/react';
import { QuestionAndAnswer } from '@carbon/pictograms-react';
import { ChatBot, UserAvatar, Send } from "@carbon/react/icons";
import loadingImage from "../assets/loading.gif";
import { useTranslation } from 'react-i18next';
import ClosedQuestions from './ClosedQuestions';

const closedQuestionsDemo = {
    questions: [{
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the requester.fiscalID",
        "labels": [
            { "locale": "en", "text": "what is the fiscal ID of the requester?" },
            { "locale": "fr", "text": "quel est l'identifiant fiscal du demandeur ?" }
        ],
        "data_type": "Text",
        "restrictions": {
            "range": null,
            "text": { "regex": "\\b[0-9]{9}\\b", "minLength": 1, "maxLength": 10 },
            "enumeration": null
        },
        "default_value": "1234567890"
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the requester.Eiffel",
        "labels": [
            { "locale": "en", "text": "what is heigth of the Eiffel Tower?" },
            { "locale": "fr", "text": "Quelle est la hauteur de la Tour Eiffel ?" }
        ],
        "data_type": "Integer",
        "restrictions": {
            "range": { "min": 100, "max": 1000, "step": 1 },
            "text": null,
            "enumeration": null
        },
        "default_value": 12
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the requester.Pi",
        "labels": [
            { "locale": "en", "text": "What is the value of Pi?" },
            { "locale": "fr", "text": "Quelle est la valeur de Pi ?" }
        ],
        "data_type": "Number",
        "restrictions": {
            "range": { "min": 3, "max": 4, "step": 0.0001 },
            "text": null,
            "enumeration": null
        },
        "default_value": 3.1
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the declaration.birth",
        "labels": [
            { "locale": "en", "text": "what is your birth date?" }
        ],
        "data_type": "Date",
        "restrictions": null,
        "default_value": "1970-01-01"
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the declaration.time",
        "labels": [
            { "locale": "fr", "text": "A quel instant, a eu lieu l'intrusion?" }
        ],
        "data_type": "DateTime",
        "restrictions": {
            "range": { "min": "2024-07-31T17:00", "max": "2024-08-01T08:59" },
            "text": null,
            "enumeration": null
        },
        "default_value": "2024-07-31T17:00"
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the customer.multipleContracts",
        "labels": [
            { "locale": "en", "text": "Does the customer have another contract?" },
            { "locale": "fr", "text": "Est-ce que le client a un autre contrat ?" }
        ],
        "data_type": "Boolean",
        "restrictions": null,
        "default_value": false
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the declaration.type",
        "labels": [
            { "locale": "en", "text": "what is the type of the car tax reduction request? " },
            { "locale": "fr", "text": "quel est le type de demande de remise fiscale sur véhicule ? " }
        ],
        "data_type": "Text",
        "restrictions": {
            "range": null,
            "text": null,
            "enumeration": { "possible_values": [{ "value": "HorseTrailer", "labels": [{ "locale": "en", "text": "Horse trailer" }, { "locale": "fr", "text": "Remorque à chevaux" }] }, { "value": "Camper", "labels": [{ "locale": "en", "text": "Camper" }, { "locale": "fr", "text": "Camping-car" }] }] }
        },
        "default_value": null
    }],
    isBot: true,
    closedQuestions: true
};
const closedQuestionsDemoTxt = {
    questions: [{
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the requester.fiscalID",
        "labels": [
            { "locale": "en", "text": "what is the fiscal ID of the requester?" },
            { "locale": "fr", "text": "quel est l'identifiant fiscal du demandeur ?" }
        ],
        "data_type": "Text",
        "restrictions": {
            "range": null,
            "text": { "regex": "\\b[0-9]{9}\\b", "minLength": 1, "maxLength": 10 },
            "enumeration": null
        },
        "default_value": "1234567890"
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the declaration.type",
        "labels": [
            { "locale": "en", "text": "what is the type of the car tax reduction request? " },
            { "locale": "fr", "text": "quel est le type de demande de remise fiscale sur véhicule ? " }
        ],
        "data_type": "Text",
        "restrictions": {
            "range": null,
            "text": null,
            "enumeration": { "possible_values": [{ "value": "HorseTrailer", "labels": [{ "locale": "en", "text": "Horse trailer" }, { "locale": "fr", "text": "Remorque à chevaux" }] }, { "value": "Camper", "labels": [{ "locale": "en", "text": "Camper" }, { "locale": "fr", "text": "Camping-car" }] }] }
        },
        "default_value": null
    }],
    isBot: true,
    closedQuestions: true
};

const closedQuestionsDemoNum = {
    questions: [{
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the requester.Eiffel",
        "labels": [
            { "locale": "en", "text": "what is heigth of the Eiffel Tower?" },
            { "locale": "fr", "text": "Quelle est la hauteur de la Tour Eiffel ?" }
        ],
        "data_type": "Integer",
        "restrictions": {
            "range": { "min": 100, "max": 1000, "step": 1 },
            "text": null,
            "enumeration": null
        },
        "default_value": 0
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the requester.Pi",
        "labels": [
            { "locale": "en", "text": "What is the value of Pi?" },
            { "locale": "fr", "text": "Quelle est la valeur de Pi ?" }
        ],
        "data_type": "Number",
        "default_value": 3.1
    }],
    isBot: true,
    closedQuestions: true
};

const closedQuestionsDemoDate = {
    questions: [{
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the declaration.birth",
        "labels": [
            { "locale": "en", "text": "what is your birth date?" }
        ],
        "data_type": "Date",
        "restrictions": { "range": { "min": "1924-09-15", "max": "2006-09-15" } },
        "default_value": "2006-08-31"
    },
    {
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the declaration.time",
        "labels": [
            { "locale": "fr", "text": "A quel instant, a eu lieu l'intrusion?" }
        ],
        "data_type": "DateTime",
        "restrictions": {
            "range": { "min": "2024-09-05T17:00", "max": "2024-09-15T08:59" },
            "text": null,
            "enumeration": null
        },
        "default_value": "2024-07-31T17:00"
    }],
    isBot: true,
    closedQuestions: true
};

const closedQuestionsDemoBool = {
    questions: [{
        "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the customer.multipleContracts",
        "labels": [
            { "locale": "en", "text": "Does the customer have another contract?" },
            { "locale": "fr", "text": "Est-ce que le client a un autre contrat ?" }
        ],
        "data_type": "Boolean",
        "restrictions": null,
        "default_value": false
    }],
    isBot: true,
    closedQuestions: true
};


const OwlAgent = ({ backendBaseAPI, agent, openState, setOpenState, randomNumber }) => {
    const { t, i18n } = useTranslation();

    // Ref for scrolling to the end of messages
    const msgEnd = useRef(null);

    // State variables
    const [input, setInput] = useState("");
    const [useFileSearch, setUseFileSearch] = useState(true); // eslint-disable-line
    const [resetHistory, setResetHistory] = useState(false);
    const [reenterInto, setReenterInto] = useState("");
    const [threadId, setThreadId] = useState(null);
    const [userId, setUserId] = useState("");

    const [lastMessage, setLastMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);

    const inputRef = useRef(null);

    useEffect(() => {
        if (inputRef.current) {
            inputRef.current.focus();
        }
    }, [randomNumber]);

    useEffect(() => {
        // Random user id
        const uniqueId = `user_${Math.random().toString(36).substr(2, 9)}_${Date.now()}`;
        setUserId(uniqueId);
    }, []);

    useEffect(() => {
        // Scroll to the end of messages when messages change
        console.log("Scroll to the end of messages", messages);
        msgEnd.current.scrollIntoView();
    }, [messages]);

    useEffect(() => {
        console.log("AgentId=", agent.agent_id)
        setResetHistory(true);
        setThreadId(null);
        setReenterInto("");
        setMessages([{ text: "Welcome to the " + (agent.name ? agent.name : agent.agent_id) + ". How can I help you today?", isBot: true }]);
    }, [agent]);

    const informUser = (message) => {
        // Inform the user
        console.log("informUser: " + message);
        if (message === "---Restart conversation---") {
            setResetHistory(true);
            setThreadId(null);
            setMessages([...messages, { text: "Clear", isBot: true }]);
        } else {
            setMessages([...messages, { text: message, isBot: true }]);
        }
    }

    const localizedLabel = (keyname) => {
        const questions = messages[messages.length - 1].questions;
        let text = "";
        let answer = questions.find(question => question.key_name === keyname);
        if (answer?.labels?.length > 0) {
            let label = answer.labels.find(label => label.locale === i18n.language);
            if (label) {
                text = label.text;
            } else {
                text = answer.labels[0].text;
            }
        } else {
            text = answer.key_name + ":";
        }

        return text;
    }

    const submitMessage = async (type, closedQuestionAnswers) => {
        // type=user: Submit user message to the server
        // type=closedAnswers: Submit closed questions answers to the server
        let text = "";
        if (type === "user") {
            text = input.trim();
            setInput("");
            setLastMessage(text);
        } else {
            console.log("submitMessage: closedAnswers=" + JSON.stringify(closedQuestionAnswers));
            text = "**Here are the answers:**\n" +
                closedQuestionAnswers.map((answer) => ("- " + localizedLabel(answer.key_name) + " `" + answer.input + "`")).join("\n");
        }
        const message = { text: text, isBot: false };
        setMessages([...messages, message]);
        setTimeout(() => { setMessages([...messages, message, { text: "...", isBot: true }]) }, 400);

        const body = {
            "locale": i18n.language,
            "query": (type === "user") ? text : "",
            "closed_answers": (type === "closedAnswers") ? closedQuestionAnswers : [],
            "reenter_into": reenterInto,
            "reset": resetHistory,
            "callWithVectorStore": useFileSearch,
            "user_id": userId,
            "agent_id": agent.agent_id,
            "thread_id": threadId,
            "chat_history": (resetHistory ? [] : chatHistory)
        }
        console.log("submitMessage: " + JSON.stringify(body));
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
            body: JSON.stringify(body)
        };

        fetch(backendBaseAPI + "c/generic_chat", requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("submitMessage: " + JSON.stringify(data));
                let answer = [];
                let closedQuestions = [];

                if (data.status === 200) {
                    answer = data.messages;
                    closedQuestions = data.closed_questions || [];

                    // setChatHistory([...chatHistory, { "role": "human", "content": text }, { "role": "AI", "content": answer }]);
                    setThreadId(data.thread_id)
                    setChatHistory(data.chat_history)
                    setReenterInto(data.reenter_into);
                    setResetHistory(false);
                } else {
                    // Error 500 or other
                    answer = [{ content: "Status http " + data.status + ": " + data.message + "\n" + data.error, style_class: "chat-msg-error" }];
                }

                let newMessages = [];
                if (answer.length > 1) {
                    let content = "<div>";
                    answer.forEach((a) => {
                        if (a?.style_class !== "") {
                            content += "<div class='" + a.style_class + "'>" + a.content + "</div>";
                        } else {
                            content += "<div>" + a.content + "</div>";
                        }
                    });
                    content += "</div>";
                    newMessages = [message, { text: content, type: "html", className: "", time: undefined, isBot: true }];
                } else {
                    newMessages = [message, { text: answer[0].content, className: answer[0].style_class, time: undefined, isBot: true, }];
                }
                if (closedQuestions.length > 0) {
                    newMessages.push({ questions: closedQuestions, isBot: true, closedQuestions: true });
                    console.log("submitMessage: closedQuestions=" + JSON.stringify(closedQuestions));
                }
                setTimeout(() => { setMessages([...messages, ...newMessages]); }, 500);
            })
            .catch(error => {
                console.error('error', error)
                setTimeout(() => {
                    setMessages([...messages, message, { text: t("app.err.handlingYourRequest"), className: "chat-msg-error", isBot: true }])
                }, 2500)
            })
    };

    const sendClosedAnswers = (answers) => {
        submitMessage("closedAnswers", answers);
    }

    const handleSend = async () => {
        // Handle send button click
        if (input) {
            await submitMessage("user");
        }
    };

    const handleEnter = async (e) => {
        // Handle enter key press: Enter to submit message, Shift+Enter to add a new line
        if (e.key === "Enter" && !e.shiftKey) {
            await handleSend();
        }
        // Arrow Up to get last message
        if ((e.key === "ArrowUp") && (input.trim() === "")) {
            setInput(lastMessage);
        }
    };

    const handleChangeInput = (e) => {
        //const value = e.target.value;
        if (e.target.value.trim() === "demo" && window?._env_?.REACT_APP_DEMO_TEXT) {
            e.target.value = window._env_.REACT_APP_DEMO_TEXT;
        } else {
            if (e.target.value.trim() === "cqdemo") {
                setLastMessage("cqdemo");
                e.target.value = "";
                setMessages([...messages, closedQuestionsDemo]);
            } else if (e.target.value.trim() === "cqtxt") {
                setLastMessage("cqtxt");
                e.target.value = "";
                setMessages([...messages, closedQuestionsDemoTxt]);
            } else if (e.target.value.trim() === "cqnum") {
                setLastMessage("cqnum");
                e.target.value = "";
                setMessages([...messages, closedQuestionsDemoNum]);
            } else if (e.target.value.trim() === "cqdate") {
                setLastMessage("cqdate");
                e.target.value = "";
                setMessages([...messages, closedQuestionsDemoDate]);
            } else if (e.target.value.trim() === "cqbool") {
                setLastMessage("cqbool");
                e.target.value = "";
                setMessages([...messages, closedQuestionsDemoBool]);
            }
        };
        setInput(e.target.value);
    }

    const restoreTextInputHeight = () => {
        inputRef.current.style.height = "100px";
    }

    return (
        <Modal open={openState}
            onRequestClose={() => setOpenState(false)}
            modalHeading={agent.name ? agent.name : agent.agent_id}
            passiveModal
            size='lg'
            preventCloseOnClickOutside
            hasScrollingContent
            className="owl-agent-modal">

            <QuestionAndAnswer style={{ width: '5rem', height: 'auto', padding: "0.5rem" }} />

            <div className="owl-agent-chats">
                {messages.map((message, i) =>
                    <div key={i} className={message.isBot ? "chat-system-message" : "chat-user-message"}>
                        {message.isBot ?
                            <ChatBot className="chat-icon" /> :
                            <UserAvatar className="chat-icon" />}
                        {(message.closedQuestions && message.questions.length > 0) ? <div className="closed-questions">
                            <ClosedQuestions lastMessage={i === messages.length - 1} questions={message.questions} feedback={sendClosedAnswers} />
                        </div> :
                            message.text === "Clear" ?
                                <div>
                                    New conversation started
                                    <br />
                                    <br />
                                    <button className="app-button" onClick={() => setMessages([{ text: "Welcome to the " + (agent.name ? agent.name : agent.agent_id) + ". How can I help you today?", isBot: true }])}>Clear chat</button>
                                </div> :
                                message.text === "..." ?
                                    <div className="waiting-for-response"><img src={loadingImage.src} alt="Loading..." /> </div> :
                                    message.type === "html" ?
                                        <div dangerouslySetInnerHTML={{ __html: message.text }} /> :
                                        message.className && message.className !== "" ?
                                            <div className={message.className}>{message.text}</div> :
                                            <div>
                                                {message.text.split('\n').map((line, j) =>
                                                    line === "" ? <br key={j} /> :
                                                        <div key={j}>
                                                            <ReactMarkdown>{line}</ReactMarkdown>
                                                        </div>
                                                )}
                                                {message.time && <div>
                                                    <br />
                                                    <div className="response-time">{"Response in " + message.time + "s"}</div>
                                                </div>}
                                            </div>}
                    </div>
                )}
                <div ref={msgEnd} />
            </div>
            <hr className="horizontal-line" onDoubleClick={restoreTextInputHeight} />
            <div className="owl-agent-input" style={{ visibility: messages[messages.length - 1]?.closedQuestions ? "hidden" : "visible" }}>
                <TextArea ref={inputRef}
                    placeholder="Enter your message here"
                    value={input}
                    rows={3}
                    onChange={handleChangeInput}
                    onKeyDown={handleEnter} />
                <Send style={{ cursor: "pointer" }} size={30} onClick={handleSend} />
            </div>
            <hr className="horizontal-line" />
        </Modal >
    );
};

export default OwlAgent;
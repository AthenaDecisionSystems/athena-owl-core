import React, { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Modal, TextArea } from '@carbon/react';
import { QuestionAndAnswer } from '@carbon/pictograms-react';
import { ChatBot, UserAvatar, Send } from "@carbon/react/icons";
import loadingImage from "../assets/loading.gif";
import { context } from '../providers';

const OwlAgent = ({ assistant, openState, setOpenState, randomNumber }) => {
    const ctx = context();

    // Ref for scrolling to the end of messages
    const msgEnd = useRef(null);

    // State variables
    const [input, setInput] = useState("");
    const [lastMessage, setLastMessage] = useState("");
    const [messages, setMessages] = useState([{ text: "Welcome to the Owl Agent. How can I help you today?", isBot: true }]);
    const [chatHistory, setChatHistory] = useState([]);
    const [resetHistory, setResetHistory] = useState(false);
    const [threadId, setThreadId] = useState(null);
    const [userId, setUserId] = useState("");

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
        msgEnd.current.scrollIntoView();
    }, [messages]);

    /* 
    useEffect(() => {
        console.log("App.js: assistantId=", assistantId, " assistantIdWithoutRules=", assistantIdWithoutRules)
    }, [assistantId, assistantIdWithoutRules]);
    */

    useEffect(() => {
        console.log("AsistantId=", assistant.assistant_id)
        setResetHistory(true);
        setThreadId(null);
        setMessages([{ text: "Welcome to the Owl Agent. How can I help you today?", isBot: true }]);
    }, [assistant]);

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

    const submitMessage = async () => {
        // Submit user message to the server
        const text = input.trim();
        setInput("");
        setLastMessage(text);
        setMessages([...messages, { text, isBot: false }]);
        setTimeout(() => { setMessages([...messages, { text, isBot: false }, { text: "...", isBot: true }]) }, 400);

        const body = {
            "locale": "en",
            "query": text,
            "reset": resetHistory,
            "user_id": userId,
            "assistant_id": assistant.assistant_id,
            "thread_id": threadId,
            "chat_history": (resetHistory ? [] : chatHistory)
        }

        console.log("submitMessage: ", body);

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
            body: JSON.stringify(body)
        };

        fetch(ctx.env.backendBaseAPI + "c/generic_chat", requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("submitMessage: " + JSON.stringify(data));
                let answer = ""
                if (data.status === 200) {
                    answer = data.message
                    // setChatHistory([...chatHistory, { "role": "human", "content": text }, { "role": "assistant", "content": answer }]);
                    setThreadId(data.thread_id)
                    setChatHistory(data.chat_history)
                    setResetHistory(false);
                } else {
                    // Error 500 or other
                    answer = "Status http " + data.status + ": " + data.message + "\n" + data.error
                }
                setTimeout(() => {
                    setMessages([
                        ...messages,
                        { text, isBot: false },
                        { text: answer, time: undefined, isBot: true }
                    ])
                }, 500);
            })
            .catch(error => {
                console.error('error', error)
                setTimeout(() => {
                    setMessages([...messages, { text, isBot: false }, {
                        text: "Error handling your request", isBot: true
                    }])
                }, 2500)
            })
    };

    const handleSend = async () => {
        // Handle send button click
        if (input) {
            await submitMessage();
        }
    };

    const handleEnter = async (e) => {
        // Handle enter key press: Enter to submit message, Shift+Enter to add a new line
        if (e.key === "Enter" && !e.shiftKey) await handleSend();
        // Arrow Up to get last message
        if ((e.key === "ArrowUp") && (input.trim() === "")) setInput(lastMessage);
    };

    const handleChangeInput = (e) => {
        if (e.target.value.trim() === "demo") {
            e.target.value = ctx.env.demoText;
        }
        setInput(e.target.value)
    };

    return (
        <Modal open={openState}
            onRequestClose={() => setOpenState(false)}
            modalHeading={"Owl Agent - " + assistant.name + " (" + assistant.assistant_id + ")"}
            passiveModal
            size='lg'
            preventCloseOnClickOutside
            hasScrollingContent>

            <QuestionAndAnswer style={{ width: '5rem', height: 'auto', padding: "0.5rem" }} />

            <div className="owl-agent-chats">
                {messages.map((message, i) =>
                    <div key={i} className={message.isBot ? "chat-system-message" : "chat-user-message"}>
                        {message.isBot ?
                            <ChatBot className="chat-icon" /> :
                            <UserAvatar className="chat-icon" />}
                        {message.text === "Clear" ?
                            <div>
                                New conversation started
                                <br />
                                <br />
                                <button className="app-button" onClick={() => setMessages([{ text: "Welcome to the Owl Agent. How can I help you today?", isBot: true }])}>Clear chat</button>
                            </div> :
                            message.text === "..." ?
                                <div className="waiting-for-response"><img src={loadingImage.src} alt="Loading..." /> </div> :
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
            <hr className="horizontal-line" />
            <div className="owl-agent-input">
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
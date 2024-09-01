// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import './App.css';

// Import Assets
import clientLogo from './assets/ibu-logo2.png';
import owlLogo from "./assets/owl.png";
import chatbotLogo from "./assets/chatbot.png";
import configIcon from "./assets/config.png";
import userIcon from './assets/avatar2.png';
import sendBtn from './assets/send.svg';
import loadingImage from "./assets/loading.gif";

// Import React Components
import { Suspense, useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useSelector, useDispatch } from 'react-redux';
import { setError } from './reducer/error.action';
import Configuration from './Configuration';
import Agent from './Agent';
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
    "default_value": 0
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
    "question_id": "4cf3f2a0-862a-4340-86d3-47099321e293", "key_name": "the declaration.isSigned",
    "labels": [
      { "locale": "en", "text": "what is isSigned?" }
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

function App() {
  // Redux state variables
  const serverUrl = useSelector((state) => state.serverUrlReducer.serverUrl);
  const error = useSelector((state) => state.errorReducer.error);

  const dispatch = useDispatch();

  const { t, i18n } = useTranslation();

  // Ref for scrolling to the end of messages
  const msgEnd = useRef(null);

  // State variables
  const [isLoading, setIsLoading] = useState(true);
  const [displayConfigurationPanel, setDisplayConfigurationPanel] = useState(false);
  const [useODM, setUseODM] = useState(false);

  const [input, setInput] = useState("");
  const [useFileSearch, setUseFileSearch] = useState(true); // eslint-disable-line
  const [resetHistory, setResetHistory] = useState(false);
  const [reenterInto, setReenterInto] = useState("");
  const [threadId, setThreadId] = useState(null);
  const [userId, setUserId] = useState("");

  const [lastMessage, setLastMessage] = useState("");
  const [messages, setMessages] = useState([{ text: t("app.msg.welcome"), isBot: true },]);
  const [chatHistory, setChatHistory] = useState([]);
  const [closedQuestionAnswers, setClosedQuestionAnswers] = useState([]);

  const [agentId, setAgentId] = useState(window._env_.REACT_APP_AGENT_ID_WITH_RULES);
  const [agentIdWithoutRules, setAgentIdWithoutRules] = useState(window._env_.REACT_APP_AGENT_ID_WITHOUT_RULES);

  // Ref to component Agent
  // When the language changes, the Agent component must update its instructions
  const agentRef = useRef();

  useEffect(() => {
    // Random user id
    const uniqueId = `user_${Math.random().toString(36).substr(2, 9)}_${Date.now()}`;
    setUserId(uniqueId);
  }, []);

  useEffect(() => {
    setIsLoading(true);

    // Check Backend
    fetch(serverUrl + "health")
      .then(response => response.json())
      .then(data => {
        console.log("Health: " + JSON.stringify(data));
        if (data.Status === "Alive") {
          setIsLoading(false);
        }
      })
      .catch(error => {
        console.error('error', error.message)
      })
  }, [serverUrl]);

  useEffect(() => {
    // Scroll to the end of messages when messages change
    if (isLoading === false) {
      msgEnd.current.scrollIntoView();
    }
  }, [messages]); // eslint-disable-line

  useEffect(() => {
    console.log("App.js: agentId=", agentId, " agentIdWithoutRules=", agentIdWithoutRules)
  }, [agentId, agentIdWithoutRules]);

  const changeLanguage = () => {
    // This is a called by the Configuration component.
    if (agentRef && agentRef.current) {
      agentRef.current.localizeAgent(i18n.language);
    }
  }

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

  const changeUseODMStatus = (status) => {
    // Change the useODM status
    setUseODM(status);
  }

  const changeUseFileSearchStatus = (status) => {
    // Change the useFileSearch status
    setUseFileSearch(status);
  }

  const submitMessage = async () => {
    // Submit user message to the server
    const text = input.trim();
    setInput("");
    setLastMessage(text);
    setMessages([...messages, { text, isBot: false }]);
    setTimeout(() => { setMessages([...messages, { text, isBot: false }, { text: "...", isBot: true }]) }, 400);
    setError(null);
    dispatch(setError(null));

    const body = {
      "locale": i18n.language,
      "query": text ? text : closedQuestionAnswers,
      "reenter_into": reenterInto,
      "reset": resetHistory,
      "callWithVectorStore": useFileSearch,
      "user_id": userId,
      "agent_id": (useODM ? agentId : agentIdWithoutRules),
      "thread_id": threadId,
      "chat_history": (resetHistory ? [] : chatHistory)
    }

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
      body: JSON.stringify(body)
    };

    fetch(serverUrl + "c/generic_chat", requestOptions)
      .then(response => response.json())
      .then(data => {
        console.log("submitMessage: " + JSON.stringify(data));
        let answer = ""
        if (data.status === 200) {
          answer = data.messages;

          // setChatHistory([...chatHistory, { "role": "human", "content": text }, { "role": "AI", "content": answer }]);
          setThreadId(data.thread_id);
          setChatHistory(data.chat_history);
          setReenterInto(data.reenter_into);
          setResetHistory(false);
          setClosedQuestionAnswers([]);
        } else {
          // Error 500 or other
          answer = [{ content: "Status http " + data.status + ": " + data.message + "\n" + data.error }]
        }
        if (text) {
          setTimeout(() => {
            const transformedAnswer = answer.map((a) => ({ text: a.content, className: a.style_class, time: undefined, isBot: true, }));
            setMessages([...messages, { text, isBot: false }, ...transformedAnswer]);

          }, 500);
        }
      })
      .catch(error => {
        console.error('error', error)
        setTimeout(() => {
          setMessages([...messages, { text, isBot: false }, { text: t("app.err.handlingYourRequest"), isBot: true }])
        }, 2500)
      })
  };

  const sendClosedAnswers = (answers) => {
    let list = answers.map((answer) => {
      return {
        "key_name": answer.key_name,
        "input": answer.input
      }
    });
    setClosedQuestionAnswers(list);

    informUser("**Your answers have been submitted** \n" + JSON.stringify(answers, null, 2));
  }

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
      e.target.value = window._env_.REACT_APP_DEMO_TEXT;
    }
    if (e.target.value.trim() === "cqdemo") {
      e.target.value = "";
      setMessages([...messages, closedQuestionsDemo]);
    }
    setInput(e.target.value)
  };

  const handleConfiguration = () => {
    // Handle configuration icon click
    setDisplayConfigurationPanel(!displayConfigurationPanel);
  };

  const dismissConfigurationIfDisplayed = (e) => {
    // Dismiss configuration panel if displayed and user clicks outside of it
    if (displayConfigurationPanel && !e.target.closest('.configuration-panel')) {
      setDisplayConfigurationPanel(false);
    }
  };

  if (isLoading) {
    return (
      <div className='upperSide brand'>
        <div className="configuration"><img src={configIcon} onClick={handleConfiguration} alt={t("app.alt.configuration")} /></div>
        <div className={displayConfigurationPanel ? "visible" : "hidden"}>
          <Configuration onDismiss={handleConfiguration}
            agentId={agentId}
            agentIdWithoutRules={agentIdWithoutRules}
            onChangeLanguage={changeLanguage}
            setAgentId={setAgentId}
            setAgentIdWithoutRules={setAgentIdWithoutRules} /></div>
        <div>
          {t("app.msg.loading")}
          <div className="loader"><img src={loadingImage} alt={t("app.msg.loading")} /></div>
        </div>
      </div>
    )
  }

  return (
    <div className={useODM ? "App app-owl" : "App"} onClick={dismissConfigurationIfDisplayed}>
      <Suspense fallback={null}>
        <div className="sideBar">
          <div className="configuration"><img src={configIcon} onClick={handleConfiguration} alt={t("app.alt.configuration")} /></div>
          <div className={displayConfigurationPanel ? "visible" : "hidden"}>
            <Configuration onDismiss={handleConfiguration}
              agentId={agentId}
              agentIdWithoutRules={agentIdWithoutRules}
              onChangeLanguage={changeLanguage}
              setAgentId={setAgentId}
              setAgentIdWithoutRules={setAgentIdWithoutRules} /></div>

          <div className="upperSide">
            {/* Change the logo, the className, and the brand text */}
            <div className="upperSideTop-ibu-assu">
              <img src={clientLogo} alt="Logo" className="logo-ibu-assu" />
              <span className={useODM ? "brand brand-owl" : "brand"}>
                {/* t("app.lbl.brand") */}
                {window._env_.REACT_APP_OWL_AGENT_NAME}
              </span>
            </div>

            <Agent ref={agentRef}
              agentId={(useODM ? agentId : agentIdWithoutRules)}
              informUser={informUser}
              changeUseODMStatus={changeUseODMStatus}
              changeUseFileSearchStatus={changeUseFileSearchStatus} />

            {error && <div className={useODM ? "app-error color-black" : "app-error"}>{error}</div>}
          </div>
        </div>
        <div className="main">
          <div className="chats">
            {messages.map((message, i) =>
              <div key={i} className={message.isBot ? "chat bot" : (useODM ? "chat color-black" : "chat")}>
                <img src={message.isBot ? (useODM ? owlLogo : chatbotLogo) : userIcon} alt="" className="chatImg" />
                {message.closedQuestions ? <div className="closed-questions">
                  <ClosedQuestions lastMessage={i === messages.length - 1} questions={message.questions} feedback={sendClosedAnswers} />
                </div> :
                  message.text === "Clear" ?
                    <div>
                      {t("app.msg.newThreadCreated")}
                      <br />
                      <br />
                      <button className="app-button" onClick={() => setMessages([{ text: t("app.msg.welcome"), isBot: true }])}>{t("app.btn.restartConversation")}</button>
                    </div> :
                    message.text === "..." ?
                      <div className="loader"><img src={loadingImage} alt={t("app.msg.loading")} /> </div> :
                      <div>
                        {message.text.split('\n').map((line, j) =>
                          line === "" ? <br key={j} /> :
                            <div key={j}>
                              <ReactMarkdown>{line}</ReactMarkdown>
                            </div>
                        )}
                        {message.time && <div>
                          <br />
                          <div className="response-time">{t("app.msg.responseTime", { seconds: message.time })}</div>
                        </div>}
                      </div>
                }
              </div>
            )}
            <div ref={msgEnd} />
          </div>
          <div className="chatFooter" style={{ visibility: messages[messages.length - 1].closedQuestions === undefined ? "visible" : "hidden" }}>
            <hr className="sep" />
            <div className="inp">
              <textarea
                placeholder={t("app.msg.enterYourMessage")}
                value={input}
                rows={10}
                onChange={handleChangeInput}
                onKeyDown={handleEnter} />
              <button className="send" onClick={handleSend}><img src={sendBtn} alt={t("app.alt.send")} title={t("app.alt.send")} /></button>
            </div>
          </div>
        </div>
      </Suspense>
    </div>
  );
}

export default App;
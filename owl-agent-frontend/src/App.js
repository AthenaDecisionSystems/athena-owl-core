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
import Assistant from './Assistant';
import { useTranslation } from 'react-i18next';

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
  const [useFileSearch, setUseFileSearch] = useState(true); // eslint-disable-line
  const [resetHistory, setResetHistory] = useState(false);

  const [input, setInput] = useState("");
  const [lastMessage, setLastMessage] = useState("");
  const [messages, setMessages] = useState([{ text: t("app.msg.welcome"), isBot: true }]);
  const [chatHistory, setChatHistory] = useState([]);

  const [assistantId, setAssistantId] = useState(window._env_.REACT_APP_ASSISTANT_ID_WITH_RULES);
  const [assistantIdWithoutRules, setAssistantIdWithoutRules] = useState(window._env_.REACT_APP_ASSISTANT_ID_WITHOUT_RULES);
  const [threadId, setThreadId] = useState(null);
  const [userId, setUserId] = useState("");

  // Ref to component Assistant
  // When the language changes, the Assistant component must update its instructions
  const assistantRef = useRef();

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
    console.log("App.js: assistantId=", assistantId, " assistantIdWithoutRules=", assistantIdWithoutRules)
  }, [assistantId, assistantIdWithoutRules]);

  const changeLanguage = () => {
    // This is a called by the Configuration component.
    if (assistantRef && assistantRef.current) {
      assistantRef.current.localizeAssistant(i18n.language);
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
      "query": text,           
      "reset": resetHistory,
      "user_id": userId,
      "assistant_id": (useODM ? assistantId : assistantIdWithoutRules),
      "thread_id": threadId,
      "chat_history": (resetHistory ? [] : chatHistory)
    }

/* 

    const closed_answers_body = {
      "locale": i18n.language,
      "closed_answers": [
        {
          "key_name": "the vehicle.engine.power",
          "input": "120.0"
        },
        {
          "key_name": "the vehicle.registration_date",
          "input": "2021-10-26"
        }
      ],
      "reset": resetHistory,
      "user_id": userId,
      "assistant_id": (useODM ? assistantId : assistantIdWithoutRules),
      "thread_id": threadId,
      "chat_history": (resetHistory ? [] : chatHistory)
    }

    fetch(serverUrl + "c/closed_answers", requestOptions)


*/

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
          answer = data.message  //TODO JM-JCJ: or data.closed_questions (in data, )  <============================

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
            text: t("app.err.handlingYourRequest"), isBot: true
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
      e.target.value = window._env_.REACT_APP_DEMO_TEXT;
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
            assistantId={assistantId}
            assistantIdWithoutRules={assistantIdWithoutRules}
            onChangeLanguage={changeLanguage}
            setAssistantId={setAssistantId}
            setAssistantIdWithoutRules={setAssistantIdWithoutRules} /></div>
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
              assistantId={assistantId}
              assistantIdWithoutRules={assistantIdWithoutRules}
              onChangeLanguage={changeLanguage}
              setAssistantId={setAssistantId}
              setAssistantIdWithoutRules={setAssistantIdWithoutRules} /></div>

          <div className="upperSide">
            {/* Change the logo, the className, and the brand text */}
            <div className="upperSideTop-ibu-assu">
              <img src={clientLogo} alt="Logo" className="logo-ibu-assu" />
              <span className={useODM ? "brand brand-owl" : "brand"}>
                {/* t("app.lbl.brand") */}
                {window._env_.REACT_APP_OWL_AGENT_NAME}
              </span>
            </div>

            <Assistant ref={assistantRef}
              assistantId={(useODM ? assistantId : assistantIdWithoutRules)}
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
                {message.text === "Clear" ?
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
                    </div>}
              </div>
            )}
            <div ref={msgEnd} />
          </div>
          <div className="chatFooter">
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
            <p className={useODM ? "color-background-with-odm" : "color-background-without-odm"}>{t("app.msg.chatGPTCanMakeMistakes")}</p>
          </div>
        </div>
      </Suspense>
    </div>
  );
}

export default App;
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
  const [useFileSearch, setUseFileSearch] = useState(true);
  const [resetHistory, setResetHistory] = useState(false);

  const [input, setInput] = useState("");
  const [lastMessage, setLastMessage] = useState("");
  const [messages, setMessages] = useState([{ text: t("app.msg.welcome"), isBot: true }]);
  //  const [chatHistory, setChatHistory] = useState([]);

  const [promptRef, setPromptRef] = useState("openai_insurance_with_tool");
  const [modelParameters, setModelParameters] = useState({
    "modelName": "gpt-4o",
    "modelClass": "agent_openai",
    "temperature": 0,
    "top_k": 1,
    "top_p": 1
  });

  // Ref to component Assistant
  // When the language changes, the Assistant component must update its instructions
  const assistantRef = useRef();

  useEffect(() => {
    // Check Backend
    fetch(serverUrl + "health")
      .then(response => response.json())
      .then(data => {
        console.log("useEffect: " + JSON.stringify(data));
        if (data.Status === "Alive") {
          setIsLoading(false);
        }
      })
      .catch(error => {
        console.log('error', error.message)
      })
  }, []); // eslint-disable-line

  useEffect(() => {
    // Scroll to the end of messages when messages change
    if (isLoading === false) {
      msgEnd.current.scrollIntoView();
    }
  }, [messages]); // eslint-disable-line

  /*
    useEffect(() => {
      console.log("useEffect: chatHistory=" + JSON.stringify(chatHistory));
    }, [chatHistory]);
  */

  const changeLanguage = () => {
    // This is a called by the Configuration component.
    console.log("changeLanguage: Language changed to " + i18n.language);

    // Create new assistant (using the new language)
    console.log("changeLanguage: assistantRef:", assistantRef)
    if (assistantRef && assistantRef.current) {
      assistantRef.current.localizeAssistant();
    }
  }

  const informUser = (message) => {
    // Inform the user
    console.log("informUser: " + message);
    if (message === "---Restart conversation---") {
      setResetHistory(true);
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
      "callWithVectorStore": useFileSearch,
      "callWithDecisionService": useODM,
      "locale": i18n.language,
      "query": text,
      "type": "chat",
      "reset": resetHistory,
      "prompt_ref": promptRef,
      "modelParameters": modelParameters,
      "chat_history": [] // chatHistory
    }
    if (resetHistory) {
      console.log("submitMessage: resetHistory=" + resetHistory);
    }

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'accept': 'application/ json' },
      body: JSON.stringify(body)
    };

    fetch(serverUrl + "c/generic_chat", requestOptions)
      .then(response => response.json())
      .then(data => {
        console.log("submitMessage: " + JSON.stringify(data));
        let answer = ""
        if (data.status === 200) {
          answer = data.message
          // setChatHistory([...chatHistory, { "role": "human", "content": text }, { "role": "assistant", "content": answer }]);
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
        console.log('error', error)
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

  const handleConfiguration = () => {
    // Handle configuration icon click
    setDisplayConfigurationPanel(!displayConfigurationPanel);
  };

  const changeModelParameters = (value) => {
    setModelParameters(value);
  }

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
        <div className={displayConfigurationPanel ? "visible" : "hidden"}><Configuration onDismiss={handleConfiguration} onChangeLanguage={changeLanguage} onChangeModelParameters={changeModelParameters} /></div>
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
          <div className={displayConfigurationPanel ? "visible" : "hidden"}><Configuration onDismiss={handleConfiguration} onChangeLanguage={changeLanguage} onChangeModelParameters={changeModelParameters} /></div>

          <div className="upperSide">
            {/* Change the logo, the className, and the brand text */}
            <div className="upperSideTop-ibu-assu">
              <img src={clientLogo} alt="Logo" className="logo-ibu-assu" />
              <span className={useODM ? "brand brand-owl" : "brand"}>{t("app.lbl.brand")}</span>
            </div>

            <Assistant ref={assistantRef} informUser={informUser} changeUseODMStatus={changeUseODMStatus} changeUseFileSearchStatus={changeUseFileSearchStatus} />

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
                onChange={(e) => setInput(e.target.value)}
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
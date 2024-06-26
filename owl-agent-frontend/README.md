Copyright 2024, Athena Decision Systems

@author Joel Milgram

---

# This is the OWL Frontend

It enables access to your custom demo based on the Owl Backend.  The demos are in this [Git repository](https://github.com/AthenaDecisionSystems/athena-owl-demos).

The Frontend is developped in Javascript and leverages the [React library](https://react.dev/).

To run it, two options (detailed below):
1. As a Docker container
2. With [Node.js Javascript runtime environment](https://nodejs.org/)

> Choose option 2. if you plan to modify the Frontend's code.

---

### Git archive: [athena-owl-core/owl-agent-frontend](https://github.com/AthenaDecisionSystems/athena-owl-core/tree/main/owl-agent-frontend)


## 1. As a Docker container

> In the `owl-agent-frontend`folder, review the Dockerfile, build the Docker image and run it!

From a terminal, enter the following commands:
```
cd owl-agent-frontend
docker build -t athena/owl-frontend:latest .
docker run -d -p 3000:80 athena/owl-frontend
```

## 2. With Node.js (Javascript runtime environment)

> Install Node.js, import the packages (`npm i`) and start the Dev environment (`npm start`).

2.1. Install [Node.js](https://nodejs.org/)

2.2. From a terminal, enter the following commands:

```
cd owl-agent-frontend
npm i
npm start
```

Whenever a subsequent `git pull` changes the dependency list (`package.json`), then the command `npm i`, that installs packages, must be launched again.

---

Invoke the Frontend from your browser: [http://localhost:3000](http://localhost:3000).


---

## Parameters and customization

The Frontend assumes that the Backend runs on port 8000. Edit the parameter `REACT_APP_BACKEND_URL` or go to the Frontend's configuration panel to change it. This parameter is the full base line URL for the backend's APIs: `http://backend-server:backend-port/api/v1/`.

When you build your own custom solution, you can customize this Frontend with those parameters:

| Parameter | Description |
|-----------|-------------|
|REACT_APP_AGENT_NAME|Name of your agent that will be displayed just aside the IBU logo. Example: `Miniloan Management Agent`.|
|REACT_APP_BACKEND_URL|By default, this is `http://localhost:8000/api/v1/`. Adapt according to your configuration.|
|REACT_APP_ASSISTANT_ID|Id of your assistant as defined in the `ibu_backend/config/assistants.yaml` file. For Miniloan, this is `ibu_assistant`.|
|REACT_APP_AGENT_ID|Id of your agent. For Miniloan, this is `ibu_agent`.|
|REACT_APP_DEFAULT_PROMPT|This is the default prompt name. For Miniloan example, the value is `ibu_loan_prompt`.|
|REACT_APP_DEMO_TEXT|To simplify your demo, you can simply enter `demo`in the chat and the content of this parameter will be automatically inserted. Example for Miniloan: `One of our client Robert Smith wants a loan for \$500,000 for a duration of 60 months do we approve it?`|

---

> When you run the Frontend as a Docker container, edit the parameters in the Dockerfile.

> When you run it with `npm start`, define the parameters in your environment:

```
export REACT_APP_AGENT_NAME='Miniloan Management Agent'
export REACT_APP_BACKEND_URL='http://localhost:8000/api/v1/'
export REACT_APP_ASSISTANT_ID='ibu_assistant'
export REACT_APP_AGENT_ID='ibu_agent'
export REACT_APP_DEFAULT_PROMPT='ibu_loan_prompt'
export REACT_APP_DEMO_TEXT="One of our client Robert Smith wants a loan for \$500,000 for a duration of 60 months do we approve it?"
```

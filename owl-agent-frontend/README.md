Copyright 2024, [Athena Decision Systems](http://www.athenadecisions.com/)

@author [Joel Milgram](mailto:joel@athenadecisions.com)

---

# This is the OWL Frontend

The front-end is an interactive chatbot-style UI for custom demos based on the OwlAgent Backend.  The current demos are in this [Git repository](https://github.com/AthenaDecisionSystems/athena-owl-demos).

The front-end is developed in Javascript and leverages the [React library](https://react.dev/).

To run it, you have two options (detailed below):
1. As a Docker container
2. With [Node.js Javascript runtime environment](https://nodejs.org/)

> Use option 2 if you plan to modify the front end's code.

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

Whenever a subsequent `git pull` changes the dependency list (`package.json`), you need to re-execute the command `npm i`, that installs updated and new packages.

---

Invoke the front-end from your browser: [http://localhost:3000](http://localhost:3000).


---

## Parameters and customization

The front-end assumes that the back-end runs on port 8000. Edit the parameter `REACT_APP_BACKEND_URL` or go to the front-end's configuration panel to change it. This parameter is the full base line URL for the backend's APIs: `http://backend-server:backend-port/api/v1/`.

When you build your own custom solution, you can customize this Frontend with those parameters:

| Parameter | Description |
|-----------|-------------|
|REACT_APP_OWL_AGENT_NAME|Name of your OWL Agent that will be displayed just aside the IBU logo. Example: `Miniloan Management Agent`.|
|REACT_APP_BACKEND_URL|By default, this is `http://localhost:8000/api/v1/`. Adapt according to your configuration.|
|REACT_APP_ASSISTANT_ID_WITH_RULES|You should have defined several assistants in the `ibu_backend/config/assistants.yaml` file. This parameter is the name of your assistant that includes ODM calling. For Miniloan, this is `ibu_assistant`.|
|REACT_APP_ASSISTANT_ID_WITHOUT_RULES|That one is the name of your assistant that **DOES NOT** include ODM calling. For Miniloan, this is `ibu_assistant_limited`.|
|REACT_APP_DEMO_TEXT|To simplify your demo, you can simply enter `demo`in the chat and the content of this parameter will be automatically inserted. Example for Miniloan: `One of our client Robert Smith wants a loan for \$500,000 for a duration of 60 months do we approve it?`|

---

> When you run the front-end as a Docker container, edit the parameters in the `docker-compose.yaml` file or in your `.env` file.

> When you run it with `npm start`, define the parameters in your environment:

```
export REACT_APP_OWL_AGENT_NAME='Miniloan Management Agent'
export REACT_APP_BACKEND_URL='http://localhost:8000/api/v1/'
export REACT_APP_ASSISTANT_ID_WITH_RULES='ibu_assistant'
export REACT_APP_ASSISTANT_ID_WITHOUT_RULES='ibu_assistant_limited'
export REACT_APP_DEMO_TEXT="One of our client Robert Smith wants a loan for \$500,000 for a duration of 60 months do we approve it?"
```

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

> In the `owl-agent-frontend`folder, build the Docker image and run it!

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

The Frontend assumes that the Backend runs on port 8000. This is a parameter that you can edit on the Frontend's configuration panel.

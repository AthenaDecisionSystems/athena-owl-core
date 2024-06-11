Copyright 2024, Athena Decision Systems

@author Joel Milgram

---

# This is the OWL Frontend

It enables access to your custom demo based on the Owl Backend
The demos are in this [repo](https://github.com/AthenaDecisionSystems/athena-owl-demos)


## How it works

1. Install Node.js (contains npm)
2. Clone this Git archive
3. From a terminal, enter the following commands:
4. `cd owl-agent-frontend`
5. `npm i` (Sync Javascript libraries)
6. `npm start` (Run project)
7. The frontend should show up in your browser [http://localhost:3000](http://localhost:3000)
8. Each time you pull new changes, run npm i in case there are new packages to install

The front-end assumes that the backend runs on port 8000. This is a parameter that you can edit on the front-end.

Alternately, you can run the front-end as a docker image running NGinX with the Dockerfile in src/.

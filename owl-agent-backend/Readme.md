#  OWL Agent Backend Template

Created 04/01/2024 - 
Updated 6/04/24: extract insurance demo content to make it more generic
Updated 6/6/24: remove main as it should be a code template or python module. work on unit tests and content management for RAG supporting pdf, text, and markdown

This backend is based on LangChain Agent APIs. It uses FastAPI routers to defined the different APIs of an agent backend. 
It is the generic implementation without any domain specific integration or decision service. See IBU insurance for a specific implementation using this code.

To see architecture, design decisions and documentation go to the `owl--prod-doc` folder and run `mkdocs serve`.

## Requirements

* [x] Support REST API for conversation and Q&A
* [x] Support OpenAI as LLM for Q&A and Conversation interaction 
* [x] support OpenAI assistant API in a separate agent.
* [x] externalize the locale support in a separate module: .
* [ ] support Anthropic API
* [x] Support watsonX.ai API. As of now (5/22) the langchain Watson wrapper bind_tools is not yet supported. 
* [ ] Support LLama3 Ollama
* [x] support setting the locale from the UI and via API
* [ ] support setting the LLM backend from ui and via api - default is via config file
* [ ] use a dummy agent to simulate remote LLM and get all the application logic working.
* [x] automate non-regression tests
* [x] implement the RAG. Vector Store is used as backend. 
* [ ] tool to prepare a project

Checked items have unit tests (ut) running successfully. 

## Repository organization

* src folder includes Python codes for the components of the backend:

    * **llm** folder includes the different LLM wrapper classes 
    * **config** folder for the backend unique yaml config file
    * **itg.decisions** folder for decision service integration, use a dummy rule engine
    * **itg.store** folder for component related to vector store

* tests folder includes unit tests. See later section on tests.

## Pre-requisites

* Start a virtual environment python env with python 3.11 or 3.12

```sh
python -m venv .venv
# for MAC users
source ./venv/bin/activate
# for Windows
source ./venv/Scripts/activate
```

* Install dependencies for the backend from the src folder: 

```sh
pip3 install -r src/requirements.txt
```

* Install dependencies for tests

```sh
pip3 install -r tests/requirements.txt
```

## Development mode for backend

All is done in unit tests for testing generic backend. The configuration is under `tests/ut/config/config.yaml`

### Unit testings

Run all unit tests:

```sh
pytest -s tests/ut
```

## Build the docker image

If you use Docker Desktop or have a docker engine to build the image do the following command to build the backend docker images with the script:

```sh
./build/buildImage.sh
```

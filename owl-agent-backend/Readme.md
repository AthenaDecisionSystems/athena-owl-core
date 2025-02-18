#  OWL Backend

* Created 04/01/2024 - 
* Updated 6/04/24: extract insurance demo content to make it more generic
* Updated 6/6/24: remove main as it should be a code template or python module. work on unit tests and content management for RAG supporting pdf, text, and markdown
* Updated 6/13/24: Add assistant operations, and definition. 
* Update 2/17/2025: Add API to list the supported models and LLM provider

This backend is based on LangChain Agent APIs. It uses FastAPI routers to defined the different APIs of an agent backend. 
It is the generic implementation without any domain specific integration or decision service. See IBU insurance for a specific configuration of this server code.

To see the application requirements, architecture diagrams, design decisions and documentation go to the `owl--prod-doc` folder and run `mkdocs serve`.

## Requirements


* [x] Support REST API for conversation and Q&A
* [x] Support OpenAI as LLM for Q&A and Conversation interaction 
* [x] support OpenAI assistant API in a separate agent.
* [x] externalize the locale support in a separate module: .
* [ ] support Anthropic API
* [x] Support watsonX.ai API. As of now (5/22) the langchain Watson wrapper bind_tools is not yet supported. 
* [ ] Support LLama3 running on Ollama
* [x] support setting the locale from the UI and via API
* [ ] support setting the LLM backend from ui and via api - default is via config file
* [ ] use a dummy agent to simulate remote LLM and get all the application logic working.
* [x] automate non-regression tests
* [x] implement the RAG. Vector Store is used as backend. 


Committed features must have unit tests (ut) running successfully. 

## Repository organization

* src folder includes Python codes for the components of the backend:

    * **routers** to support the different REST resources.
    * **llm** folder includes the different LLM wrapper classes 
    * **config** folder for the backend unique yaml config file
    * **itg.decisions** folder for decision service integration, use a dummy rule engine
    * **itg.store** folder for component related to vector store

* tests folder includes unit tests. See later section on tests.

## Pre-requisites

For component development purpose, be sure to have docker engine and python 3.11 (Development was done on 3.12.3)

* Prepare your .env file with the different LLM provider keys

    ```
    Declare your personal keys
    OPENAI_API_KEY=---your-key---
    WATSONX_APIKEY=---your-key---
    MISTRAL_API_KEY=---your-key---
    LANGCHAIN_API_KEY=---your-key---
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
    ...
    ```

* Start a Python virtual environment

    ```sh
    python -m venv owl_venv
    # for MAC users
    source ./owl_venv/bin/activate
    # for Windows
    source ./owl_venv/Scripts/activate
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

The backend can be started using the script [src/start_backend.sh](./src/start_backend.sh). 

While developing new capability, try to adopt a test-driven development, and use the unit tests (tests/ut folder) for testing default backend. 
The backend configuration for test may be  `tests/ut/config/config.yaml` for specific tests or the default in `src/athena/config/config.yaml`

### Unit testings

Run all unit tests:

```sh
pytest -s tests/ut
```

Run specific test

```
pytest -s tests/ut/test_assistant_mgr.py
```

## Build the docker image

If you use Docker Desktop or have a docker engine to build the image do the following command to build the backend docker images with the script:

```sh
./build/buildImage.sh
```

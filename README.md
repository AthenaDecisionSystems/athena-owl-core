# [Athena OWL Core](https://athenadecisionsystems.github.io/athena-owl-core/)

OwlAgent is a framework for constructing interactive LLM-based applications (chatbots) that include support for calling external decision services via tool-calling to ensure precise decision-making at key moments by the interactive application.

The core OwlAgent framework interacts with key parts of the generative AI and decision management ecosystem including:

* LangChain, LangGraph
* Multiple large language models that support tool calling
* Multiple model hosting environments (HuggingFace, IBM watsonx.ai, Modal, AWS Bedrock) or local model hosting (e.g. using Ollama)
* Multiple BRMS systems for decision services (IBM ODM, DMOE, ADS + potentially others)

The Athena OWL Core repository includes the generic code for OWL Assistant backend and front end. Solutions can be a simple mono-agent demonstration or a complex multi-agent implementation.

[Read the documentation](https://athenadecisionsystems.github.io/athena-owl-core/)


### High Level requirement for OwlAssistant

* [ ] Ability to access information from corporate IT systems (typically databases or systems that host key corporate data such as CRM, Maximo, or ERP systems)
* [ ] Ability to leverage information found in corporate documents that help formulate responses or policy, on top of the formalized decisions made by decision services
* [ ] Ability to access decision services by providing needed input parameters from a combination of chatbot context and enterprise IS data, and by injecting the decision service output back to the LLM’s conversation context for output text generation. 
* [ ] Ability to host the chatbot in multiple environments, including public cloud, private cloud, or enterprise data center.
* [ ] Easily creating tool calls for decision services in multiple BRMS (and optimization models as well).
* [ ] Hybrid Cloud deployment

--- 

## Code explanations

### The OWL Backend

The OWL Backend is a runnable server. See [readme file](owl-agent-backend/README.md) for  code explanations and how to run the backend in default mode.

### The OWL Frontend

[Read this to run the OWL Frontend](owl-agent-frontend/README.md)  The front end can be started here and it can be used with any demo backend that is running.

## The journey to your demonstration

The current repository to manage the different demonstration is in a separate [git repository (athena-owl-demos)](https://github.com/AthenaDecisionSystems/athena-owl-demos). See the instructions to create your own demonstration from the current backend.

---

## Contribute

We welcome your contributions. There are multiple ways to contribute: report bugs and improvement suggestion, improve documentation and contribute code.
We really value contributions and to maximize the impact of code contributions we request that any contributions follow these guidelines:

The [contributing guidelines are in this note.](./CONTRIBUTING.md)

## Project Status

* [01/2024] Creation
* [05/2024] Integration of LangChain
* [06/2024] Supporting assistants, agents APIs

## Building this booklet locally

The content of this repository is written with markdown files, packaged with [MkDocs](https://www.mkdocs.org/) and can be built into a book-readable format by MkDocs build processes.

1. Install MkDocs locally following the [official documentation instructions](https://www.mkdocs.org/#installation).
1. Install Material plugin for mkdocs:  `pip install -r requirements.txt ` 
1. `mkdocs serve`
1. Go to `http://127.0.0.1:8000/` in your browser.

## Learn more about mkdocs

* [Mkdocs](https://www.mkdocs.org/)
* [Material for MkDocs](https://squidfunk.github.io/mkdocs-material)

# Athena OWL Core

OwlAgent is a framework for constructing interactive LLM-based applications (chatbots) that include support for calling external decision services via tool-calling to ensure precise decision-making at key moments by the interactive application.

The core OwlAgent framework interacts with key parts of the generative AI and decision management ecosystem including:

* LangChain, LangGraph
* Multiple large language models that support tool calling
* Multiple model hosting environments (HuggingFace, IBM watsonx.ai, Modal, AWS Bedrock) or local model hosting (e.g. using Ollama)
* Multiple BRMS systems for decision services (IBM ODM, DMOE, ADS + potentially others)

The Athena OWL Core repository includes the generic code for OWL Agent backend and front end. The backend is, as of now, a *template project* to build custom solutions. Solutions can be a simple demonstration or a complex multi-agent implementations.

### What OwlAgents are

OwlAgent includes: 

* a set of tools usable by LLM agents
* orchestration with langchain and LangGraph, 
* prompts, 
* agent definition, 
* integration layer to connect to custom data sources and business services, 
* rules to control next best action
* document storage reference and configuration to build corpus and vector store, 
* vector store, 
* LLM model reference to access via api. 

Owl Platform portal includes an agent hub, that enterprise will offer to their employees to select the best agent in the context of their process. The agent and all its components is a deployable unit, running on hybrid cloud.

### High Level requirement for OwlAgent

* [ ] Ability to access information from corporate IT systems (typically databases or systems that host key corporate data such as CRM, Maximo, or ERP systems)
* [ ] Ability to leverage information found in corporate documents that help formulate responses or policy, on top of the formalized decisions made by decision services
* [ ] Ability to access decision services by providing needed input parameters from a combination of chatbot context and enterprise IS data, and by injecting the decision service output back to the LLM’s conversation context for output text generation. 
* [ ] Ability to host the chatbot in multiple environments, including public cloud, private cloud, or enterprise data center.
* [ ] Easily creating tool calls for decision services in multiple BRMS (and optimization models as well).
* [ ] Hybrid Cloud deployment

--- 

## Code explanations

### The OWL Backend

### The OWL Frontend

[Read this to run the front-end](owl-agent-frontend/README.md)

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

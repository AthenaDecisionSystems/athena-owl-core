# Owl Agent Framework documentation

OwlAgent is a framework for constructing interactive LLM-based applications (chatbots) that include support for calling external decision services via tool-calling to ensure precise decision-making at key moments by the interactive application.

The core OwlAgent framework interacts with key parts of the generative AI and decision management ecosystem including:

* LangChain, LangGraph
* Multiple large language models that support tool calling
* Multiple model hosting environments (HuggingFace, IBM WatsonX.ai, Modal, AWS Bedrock) or local model hosting (e.g. using Ollama)
* Multiple Business Rule Management Systems for decision services (IBM ODM, DMOE, ADS + potentially others)

The main demonstration illustrates the values of this framework to help Enterprises getting better AI solution


[![alt text](https://img.youtube.com/vi/fGEU_obHM5M/0.jpg)](https://www.youtube.com/watch?v=fGEU_obHM5M)

## What is in this documentation?

### What OwlAssistants are

OwlAssistant includes: 

* a set of agents and tasks, defined in an assistant definition manifest.
* a set of tool definitions usable by LLM agents.
* an orchestration with LangGraph for stateful graph, or langchain as stateless chain.

[See architecture notes for details](arch.md).


Tools could be:

* integration layer to connect to custom data sources, business services, or decision services.
* rules to control next best action.
* document storage reference and configuration to build corpus and vector store, 
* vector store with different collections

Owl Platform portal includes assistants, agents and tools hub, that enterprise offers to their employees to select the best assistant in the context of their business processes. The OwAssistant server is a deployable unit, running on hybrid cloud.

## Contact us

We are here to help you seamlessly integrate this innovative framework into your operations. For a customized proof of concept or production deployment, feel free to reach out to the expert team at [Athena Decision Systems](https://athenadecisions.com/contact-us). With their deep industry knowledge and tailored solutions, they will ensure a smooth and successful implementation that drives tangible value for your business.

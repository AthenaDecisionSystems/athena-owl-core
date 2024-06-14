# Owl Agent Framework documentation

OwlAgent is a framework for constructing interactive LLM-based applications (chatbots) that include support for calling external decision services via tool-calling to ensure precise decision-making at key moments by the interactive application.

The core OwlAgent framework interacts with key parts of the generative AI and decision management ecosystem including:

* LangChain, LangGraph
* Multiple large language models that support tool calling
* Multiple model hosting environments (HuggingFace, IBM watsonx.ai, Modal, AWS Bedrock) or local model hosting (e.g. using Ollama)
* Multiple BRMS systems for decision services (IBM ODM, DMOE, ADS + potentially others)

## What is in this documentation?


### What OwlAssistants are

OwlAssistants includes: 

* a set of agents and tasks, defined in an assistant definition
* a set of tools usable by LLM agents
* orchestration with langchain and LangGraph, 
* prompts, 
* agent definition, 
* integration layer to connect to custom data sources and business services, 
* rules to control next best action
* document storage reference and configuration to build corpus and vector store, 
* vector store, 
* LLM model reference to access via api. 

Owl Platform portal includes an assistants, agents and tools hub, that enterprise will offer to their employees to select the best assistant in the context of their process. The OwAssistant server is a deployable unit, running on hybrid cloud.


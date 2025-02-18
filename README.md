# [Athena OWL Core](https://athenadecisionsystems.github.io/athena-docs/)

## Introduction

LLMs are great tools for processing and generating natural language across all sorts of domains.   But for enterprise applications, they are not full solutions by themselves:  They cannot reason consistently, precisely, and transparently when making critical business decisions for organizations.   Why?

First, by themselves, they do not have access to all the information needed to make critical business decisions.   Much of this information is in documents that might be stored in a content management system; the RAG (Retrieval-Augmented Generation) technique exists to help transform these documents into a vector store, index and search them to find relevant information for a specific query, and give access to that information to an LLM to generate an appropriate response to a question.

Other information is context-dependent and can be found in corporate information systems.   For example, up-to-date information about customers, employees, products, contracts, and so on need to be accessed when a question is asked that needs that information.  Tool-calling (also called function-calling) can be used to call API's or access databases to provide this information - but the LLM needs to support this capability, and the interactive agent needs to know how to structure this kind of query.   In addition, information required to make API calls or get all the needed context might not exist in the user's query, which means the AI agent needs to figure out what information is missing and how to ask for it efficiently.

Finally, policies, regulations, and other business rules control how decisions should be made; these are usually complex and change quite often.   It is simply beyond the capacity of LLMs by themselves, even fed with document information using RAG, to gather all these rules and apply them to data consistently and explainability - indeed, in most real business cases, even humans would struggle to figure them out.   These decisions are best made by decision management systems such as Business Rule Management Systems or Optimization Engines and leveraged by LLM-based AI agents.

But how to put all these pieces together to make enterprise-grade AI agents?   That is the goal of the OwlAgent framework!

## What is the OwlAgent Framework?

OwlAgent is a framework for constructing interactive LLM-based applications (chatbots) that include support for calling external decision services via tool-calling to ensure precise decision making at key moments by the interactive application.  The OwlAgent is an open source framework initially created by [Athena Decision Systems](http://athenadecisions.com/).   Please write to [contact@athenadecisions.com](mailto:contact@athenadecisions.com) if you have any questions or want to contribute!

The core OwlAgent framework interacts with key parts of the generative AI and decision management ecosystem including:

* LangChain, LangGraph to do the agent co-ordination.
* Multiple large language models that support tool calling.
* Multiple model hosting environments (HuggingFace, IBM watsonx.ai, Modal, AWS Bedrock) or local model hosting (e.g. using Ollama).
* Multiple business rule management systems (BRMS) for decision services (IBM ODM, DMOE, ADS + potentially others).
* Multiple vector databases for RAG.

The Athena OWL Core repository includes the generic code for OWL Agent back end and front end. Solutions can range from simple mono-agent demonstrations (several are provided out-of-the-box) to complex multi-agent deployable implementations.

[Read the documentation](https://athenadecisionsystems.github.io/athena-docs/)

### High level requirements for an OwlAgent

An _OwlAgent_ is an AI-based interactive agent, sometimes called a chatbot.   For the purposes of the OwlAgent Framework, such an agent needs the following capabilities:

* [ ] Ability to access decision services by providing needed input parameters from a combination of chatbot context and enterprise data pulled from information systems, and by injecting the decision service output back to the LLM’s conversation context for output text generation.   This is the key capability that makes an OwlAgent more than just a basic chatbot or document query service.
* [ ] Ability to access information from corporate IT systems (typically databases or systems that host key corporate data such as CRM, Maximo, or ERP systems) - This lets the agent make decisions in context by leveraging current data such as up-to-date customer information.
* [ ] Ability to leverage information found in corporate documents that help formulate responses or policy, on top of the formalized decisions made by decision services.   This can help provide context in decision explanations in addition to the explanations provided directly by the decision services.
* [ ] Ability to host the chatbot in multiple environments, including public cloud, private cloud, or an enterprise data center.
* [ ] Easily create tool calls for decision services in multiple BRMS (as well as calling optimization models or other symbolic reasoning systems).
* [ ] Hybrid Cloud deployment

---

## Code Overview

The agent itself is split into two parts:  The backend server which provides the REST APIs needed to manage agent instances and conversations with them, and the frontend server which provides a default user experience for interacting with the backend.   Other servers such as a decision management server (BRMS server) and a vector data store for document access might also be running.   Typically, these individual services are deployed as Docker images and can be run together to make a full agent using Docker compose or a Kubernetes cluster.

To make a new agent, you use a declarative format in a YAML file to specify what makes the agent unique:  The prompt, the tools it can call, the models and other services it uses.   This minimizes the amount of programming you need to do to make a new agent, and makes it possible for several agents to easily co-exist together in an environment.

### The Owl Backend

The OWL Backend is a runnable server. See [readme file](owl-agent-backend/README.md) for code explanation and how to run the backend in default mode.  The back end provides a REST API interface so it can be called from a variety of places.

### The Owl Frontend

[Read this to run the OWL Frontend](owl-agent-frontend/README.md)  The front end is a default interactive chatbot UI suitable for demos and simple applications that use Owlagents.  It can be started here and it can be used with any demo backend that is running.

## The journey to your demonstration

It is common to start a new project with a demonstration or POC to ensure alignment of objectives with the business stakeholders.   The OwlAgent framework comes equipeed to make this easy with several prebuilt examples and detailed instructions to make new ones.

The current repository to store the initial set of demonstrations is in a separate [git repository (athena-owl-demos)](https://github.com/AthenaDecisionSystems/athena-owl-demos). See the instructions there to create your own demonstration using the backend server.   Please feel free to store your demonstration back in the repository so others can use it as well!   If you need assistance for that, please contact [Athena Decision Systems](http://www.athenadecisions.com/) at [contact@athenadecisions.com](mailto:contact@athenadecisions.com).

---

## Contribute

We welcome your contributions! There are multiple ways to contribute: reporting bugs and suggesting improvements, improving the documentation, and contributing code fixes and new features.

We deeply value your contributions. To maximize the impact of code contributions, we request that they follow these guidelines:

The [contributing guidelines are in this note.](./CONTRIBUTING.md)

## Project Status

* [01/2024] Creation
* [05/2024] Integration of LangChain
* [06/2024] Supporting agents APIs
* [09/2024] Supporting k8s deployment


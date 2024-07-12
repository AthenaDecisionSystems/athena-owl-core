# Owl Agent Framework documentation

OwlAgent is an open source Hybrid AI framework for constructing interactive LLM-based assistants (e.g. chatbots) that include support for calling external decision services built with business rules via tool-calling to ensure precise decision-making at key moments by the interactive application. These applications can also access databases to get in-context information and a vector store of documents for doing RAG so that the chatbot can answer questions with relevant data and documents. Other tools can also be created for additional API access in the applications. This combination of technologies is called Hybrid AI and OwlAgent framework helps you create Agentic applications.

## Why this framework?

Today, most LLM-based applications in organizations focus on doing purely text-based tasks with a sprinkling of organizational knowledge from a set of documents - tasks like document or report summarization, answering questions whose answers can be found in documents, and "conversing with data" to get additional information about enterprise data.

The next generation of applications will have to make precise, accurate, explainable decisions in context, leveraging the power of LLMs for natural language understanding and generation, but applying the organization's policies, contracts, and regulations to its data to help drive the business forward.   This can be used in places like customer service to answer specific customer queries about their individual situation, helping technicians maintain large equipment, and helping to automate complex tasks that currently require a lot of human time, for example translating complex purchase orders into bills of material for manufacturing.   These tasks require more than extracting information from documents - they require understanding natural language request intentions to make precise decisions by matching the right data to the right policies precitably and reliably, with clear explanations, and reformulating those decisions in natural language to make sense to end users.

This class of applications requires a different approach, specifically for making decisions and getting the right data for those decisions.   It is not sufficient to simply ask LLMs, with their probabilistic models based on large correlations of language sequences, to reason about complex policy application decisions.   Their reasoning capabilities are not sufficient (indeed, one could argue they have none at all) and the need to get precise data to make these decisions requires additional reasoning and skill.   The best solutions will be hybrid - combining LLMs for natural language with additional tools for data management and decision-making - tools like business rules, knowledge graphs, and goal-oriented engines that know how to gather just the data needed to make decisions.

The OwlAgent framework makes it as easy as possible to combine these different elements into a single interactive application, by minimizing the amount of custom development work so develpment teams can spend more time on developing decision services and thinking about UI and other issues.   It relies on common industry substrates like LangGraph and LangChain, and lets you use a variety of LLMs, vector stores, databases, decision engines, and other back-end tools needed for operations.

The OwlAgent framework is open source and we welcome all users and contributors!   Please write to [Athena Decision Systems](mailto:contact@athenadecisions.com) if you have any questions or need any support!   We are constantly iterating the framework and we hope you can use it successfully and ideally help out yourself!

## The approach

The philosophy of the OwlAgent Framework is to be as declarative as possible, with almost all assistant components specified as parameters in a YAML file.   This greatly simplifies creating a new assistant, and allows assistants to run in a single server with a REST API.   In addition, there is a clean separation between the back end server and the front end, meaning you can write your own front end or use the assistants in a completely different type of application, simply by calling the REST APIs.

The OwlAgent Framework was initially written by [Athena Decision Systems](http://www.athenadecisions.com/) but contributions are welcome from the whole community!   If you have any questions, please reach out by emailing Athena at [contact@athenadecisions.com](mailto:contact@athenadecisions.com).

The core OwlAgent framework leverages key parts of the generative AI and decision management ecosystem including:

* LangChain, LangGraph
* Multiple large language models that support tool calling
* Multiple model hosting environments (HuggingFace, IBM WatsonX.ai, Modal, AWS Bedrock) or local model hosting (e.g. using Ollama)
* Multiple Business Rule Management Systems for decision services (IBM ODM, DMOE, ADS + potentially others)

This video demonstration illustrates the value of this framework to help enterprises leverage Hybrid AI to help make even smarter interactive applications:

[![alt text](https://img.youtube.com/vi/fGEU_obHM5M/0.jpg)](https://www.youtube.com/watch?v=fGEU_obHM5M)

The [PowerPoint deck](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/docs/assets/athena-shorter%202024-05-14.pptx) presents the solution and the approach.

## Getting Started

This repository includes the core elements of the OwlAgent Framework, while the [demonstration git repository](https://github.com/AthenaDecisionSystems/athena-owl-demos) includes how to develop solutions from the core framework, or leveraging existing demonstrations.

To get started we recommend cloning both repositories:

```sh
git clone https://github.com/AthenaDecisionSystems/athena-owl-core
git clone https://github.com/AthenaDecisionSystems/athena-owl-demos
```

And [go to the demonstration documentation](https://athenadecisionsystems.github.io/athena-owl-demos/) to run one of the existing demonstration or [build your own solution](https://athenadecisionsystems.github.io/athena-owl-demos/build_sol/).

## What is in this documentation?

### OwlAssistants

With the OwlAgent Framework, you can create assistants called OwlAssistants.   Each new use case or combination of components is an assistant.   For example, you can make an assistant for doing next best actions for customer service reps for your industry, or for helping maintenance technicians decide what inspections or maintenance operations to perform.   If you have a new decision service or domain model or functionality, you will typically make a new assistant.

An OwlAssistant includes:

* a set of agents and tasks, defined in an assistant definition manifest (a YAML file).
* a set of tool definitions usable by LLM agents.
* an orchestration with LangGraph for stateful graph, or langchain as stateless chain.

[See architecture notes for details](arch.md).

Tools can be used to:

* access an integration layer to connect to custom data sources, business services, or decision services.
* execute rules to decide and run the next best action.
* read from a document storage reference and configuration to build corpus and vector store, 
* do semantic search in a vector store with different collections,
* leverage third party API's to allow applications to take action in the world.

The Owl Platform portal includes assistants, agents, and a tools hub that enterprises can use to let employees and other stakeholders select the best assistant for their tasks. The OwAssistant server is a deployable dockerized unit that can run on any hybrid cloud platform.

You can review [the blog about moving from Generative AI to Hybrid AI](./gen_ai_gs.md).

## Contact us

Athena Decision Systems is here to help you seamlessly integrate this innovative framework into your operations. For a customized proof of concept or production deployment, feel free to reach out to the expert team at [Athena Decision Systems](https://athenadecisions.com/contact-us). With deep industry knowledge and tailored solutions, Athena can ensure a smooth and successful implementation that drives tangible value for your business.

# Owl Agent Framework documentation

OwlAgent is an open source Hybrid AI framework for constructing interactive LLM-based assistants (e.g. chatbots) that include support for calling external decision services built with business rules via tool-calling to ensure precise decision-making at key moments by the interactive application.  These applications can also access databases to get in-context information and a vector store of documents for doing RAG so that the chatbot can answer questions with relevant data and documents.   Other tools can also be created for additional API access in the applications.   This combination of technologies is called Hybrid AI.

The philosophy of the OwlAgent Framework is to be as declarative as possible, with almost all assistant components specified as parameters in a YAML file.   This greatly simplifies creating a new assistant, and allows assistants to run in a single server with a REST API.   In addition, there is a clean separation between the back end server and the front end, meaning you can write your own front end or use the assistants in a completely different type of application, simply by calling the REST API.

The OwlAgent Framework was initially written by [Athena Decision Systems](http://www.athenadecisions.com/) but contributions are welcome from the whole community!   If you have any questions, please reach out by emailing Athena at [contact@athenadecisions.com](mailto:contact@athenadecisions.com).

The core OwlAgent framework interacts with key parts of the generative AI and decision management ecosystem including:

* LangChain, LangGraph
* Multiple large language models that support tool calling
* Multiple model hosting environments (HuggingFace, IBM WatsonX.ai, Modal, AWS Bedrock) or local model hosting (e.g. using Ollama)
* Multiple Business Rule Management Systems for decision services (IBM ODM, DMOE, ADS + potentially others)

This video demonstration illustrates the value of this framework to help enterprises leverage Hybrid AI to help make even smarter interactive applications:

[![alt text](https://img.youtube.com/vi/fGEU_obHM5M/0.jpg)](https://www.youtube.com/watch?v=fGEU_obHM5M)

The [PowerPoint deck](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/docs/assets/athena-shorter%202024-05-14.pptx) presents the solution and the approach.

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

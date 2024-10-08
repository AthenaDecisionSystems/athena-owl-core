# From Generative AI to Hybrid AI

## Introduction

Generative AI uses special types of neural network models to generate new content (text, images, music, videos, and so on) based on a request that is typically text. Models are pre-trained on vast amounts of unlabeled data, using from 7B to 500B parameters. The models are trained on terabytes of data including books, articles, websites, and whatever else the model trainers can find and feel they can use. This helps the model simulate learning grammar, facts, reasoning abilities and even some level of common sense from the content - because there is a rich store of sequential patterns in the training data to draw on.

Gen AI's natural language understanding and generation capabilities applies well to different use cases: improving customer experience through natural language, improving an employee's productivity, provoking creativity by generating ideas based on identifying deep correlations in seemingly unrelated areas, and optimizing certain business processes. Overall, generative AI sometimes seems like magic - and at first it seems like Generative AI is a general intelligence because we humans always associate high level of natural language ability with high intelligence.

### Key Concepts

Generative AI today is often used via a chatbot hosted by an AI vendor like OpenAI, Anthropic, IBM, or Mistral. Most of the platforms, including IBM's `watsonx.ai`, use Large Language Models (LLM) with many query types. The architecture of such a system looks like this:

![Chatbot Architecture](./diagrams/current_chat_sandbox.drawio.png){ width=900 }

LLMs are typically hosted on dedicated hardware with GPUs that are needed for high-speed inference.  (Inference is the technical term for generating new content with a model.)  LLMs are primarily used to do natural language processing (NLP) of unstructured queries from human users. The interactions are stateless, and the concept of a context window is used to include contextual data as part of the query.   Contextual data includes previous dialog in a conversation, system prompts, relevant bits of information from other documents (called RAG), or data brought in from databases or external API service calls.  As the LLM is essentially stateless, any information used to generate a response must be included in the context, which is why context window size is very important.   Since most AI companies charge per token consumed and generated, the more context that is included in each LLM query, the more expensive the query.[^1]

[^1]: We use the term _query_, but in reality the LLM generates the next most likely tokens after the content of the context window given its training model; no database or other external data source is queried per se.  Any such external reference is done by adding more data to the context window; techniques like _tool calling_ iteratively add information to the context by calling 3rd party APIs.

![Watsonx.ai screenshot](./images/watsonx.ai.main.PNG){ width=900 }

IBM's watsonx.ai, for example, helps users select which LLM to use, define system prompts, and perform queries. As an enhanced platform, AI scientists can also fine-tune an existing open-source model, or develop brand new ML models.

The same approach exists for vendors like Anthropic, OpenAI, Perplexity, Mistral, Hugging Face, Anakin AI, AWS Bedrock, and so on.

Models used for inference are accessible via an API.

Enterprise deployments of Generative AI need a high degree integration, since enterprise applications need to leverage enterprise-specific instructions, documents, services, and data to perform useful functions for the company. Some tools are already available to help develop Generative AI workflows: For instance watsonx Orchestrate has a no-code approach for leveraging a library of skills. For developers, lower level frameworks, such as LangChain, LlamaIndex, and Haystack offer Python-based libraries with enormous flexibility and a high degree of complexity.

A typical real deployment looks like the following figure:

![Chatbot with external tools](./diagrams/current_itg.drawio.png){ width=900 }

The backend for a chatbot application needs to be integrated with existing data sources and services including databases, SOA services, Customer Relationship Management platforms, predictive machine learning models and scoring engines, business process management workflows -- and of course business-rule or optimization model based decision services... The data from these services need to be included in a conversation with a human user if it is to be relevant to the user's current context.   Fine-tuning the model with the latest information is infeasible when enterprise data changes every second and when decision models can change on a daily basis, so a dynamic approach to getting the data into the LLM's context window is needed.   In addition, in order to effect changes in the enterprise environment, the user needs to be able to update data or call services.

There are also more and more models that can be hosted for inference on smaller devices with less specialized hardware, which may have significant inference cost and performance improvements vs cloud-hosted models.  But hosting these models in an enterprise still requires creating and managing the appropriate environments and handling governance as models evolve as well as secure access to the models.

Enterprises have a heterogenous IT environment; solutions need to be deployed on virtual private clouds, on-premises servers, or in an hybrid cloud depending on the enterprise's policies and IT landscape.  Other IT considerations such as security and authentication are also paramount.

All of this means that when an enterprise wants to deploy an LLM-based solution in production, there will be significant integration and development effort.   The OwlAgent Framework attempts to minimize the development effort by providing simple abstractions and a declarative way of combining different components in a specific application.

### Challenges

LLM's are amazing tools for doing natural language processing.   But they come with challenges due to the underlying training and inference technology, due to the fact they are trained only occasionally and are thus the information they use is always out of date, and due to the fact that natural language generation is not grounded in any model of reality or reasoning but instead uses probabilistic techniques based on correlations of a huge number of strings of tokens (words). This means that hallucination and approximate retrieval are core to their architecture: the completions they generate have the same statistical distribution as the text they have been trained on. Prompt engineering cannot eliminate hallucination since the decision to assess the response as a factual completion depends on the knowledge of the prompter and requires continuously assessing all the responses.   Various techniques to reduce the impact of this lack of groundedness, such as using multiple LLMs to judge each others' answers, are expensive and only move the problem around.

* **Accuracy**: The accuracy of LLM's in answering precise questions about enterprise decisions is not acceptable to any enterprise that must follow regulations and policies and respect contractual agreements with suppliers and customers.   Because LLMs cannot truly reason or take into account regulations and policies precisely, models often produce incorrect and contradictory answers when asked for decisions or actions to undertake.  With classical ML, probabilistic output is expected and scores are combined with thresholds and rules to make final decisions. Symbolic approaches like business rules that precisely express policies produce reliable results at the cost of coding the policies mostly manually.

* **Specificity**: A single large model is unlikely to solve every business problem effectively because it is trained on generally-available information rather than enterprise-specific information. To differentiate their generative AI applications and achieve optimal performance, companies should rely on their **own data sets** tailored to their unique use case.   Even then, enterprise data changes constantly, so techniques such as RAG and tool calling are needed to leverage the most up-to-date and relevant information for a specific query.

* **Cost and Risk** of training and inference, as well as privacy and intellectual property are key concerns. LLM's can be "fine-tuned" for a specific task by using a small number of labeled examples specific to the company's industry or use case. Fine-tuned models can deliver more accurate and relevant outputs. But training and retraining models, hosting them, and doing inference with them are expensive. Cloud providers see this opportunity to sell more virtual servers equipped with GPU's at a higher price.  In addition, the fine-tuning needs to be redone and retested whenever the information used for it changes, or whenever the underlying model is updated.   Therefore, fine-tuning has only limited appeal in practice.

* **Skills**: Developing a new LLM for an enterprise usually makes little sense today, but fine tuning an existing model may in some circumstances. There are relatively few developers with expertise in model tuning, understanding their architecture and limitations, integrating them in applications, and in tuning their hyper parameters. Reinforcement learning to fine-tune existing LLM requires a huge number of trials, and data quality is still a very difficult and poorly-mastered topic.

* **Reliability and reasoning**: Generative AI models do not reason and do not plan accurately and consistently, despite multiple prompting techniques designed to get them to do so. New versions of LLMs attempt to improve this, but by design the transformer algorithm is probabilistic and greedy for text generation and does not inherently do any kind of structured symbolic reasoning or manage ontologies of concepts (knowledge graphs). LLM are very big system-1 with their knowledge based from digital representation of humanity created content.  In addition, even if they are able to make simple plans and reason over simple cases, enterprise decisions require very specific, detailed, and complex context and instructions, well beyond the capacity of any LLM reasoning techniques.  Imagine, for example, relying on chain-of-thought reasoning to get an LLM to provide expert assistance to an airplane maintenance technician on how to repair a jet engine...

For all of these reasons, we remain firmly convinced that the right way to build AI-based enterprise solutions today is by using a combination of technologies, where generative AI and LLMs play a key role, but other technologies such as symbolic rule-based decision engines are equally key.

The next sections explains the generative AI architecture in more detail.

### Transformer Architecture

**GPT-3 (Generative Pre-trained Transformer 3)** breaks the NLP boundaries with training on 175B parameters. It is built on **Transformer** which use self-**attention** mechanism to weigh the significance of different words in a sentence to understand the context in a sequence of data.

To process a text input with a transformer model, the text is **tokenized** into a sequence of words or part of words. These tokens are then **encoded** as numbers and converted into **embeddings**, which are vector-space representations of the tokens that preserve their meaning. Next, the encoder in the transformer transforms the embeddings of all the tokens into a **context vector**. Using this vector, the transformer decoder generates output based on clues. The decoder can produce the subsequent word. This process can be repeated to create an entire paragraph. This process is called **auto-regressive generation**.

The **attention** mechanism computes the similarity between tokens (the embeddings of words) in a sequence. The process keeps few tokens around each word to help understand the context. This surrounding group of tokens is called the **context window**. It is the sliding group of tokens around a word that provides contextual information. That way, the model builds an intuition of what the text is saying. The closer two words are in a vector space, the higher the attention scores they will obtain and the higher the attention they will give to each other.

The second part of the GPT-3 architecture is the set of **layers** of transformers stacked on top of each other. Within each layer, there are feed-forward neural networks to process the data.

The training has two stages: **Pre-training** where the model attempts to predict the next word in a sentence using its own corpus, and **fine tuning** where the model can be tuned for specific *tasks* or *content*. During the pre-training process, the model automatically takes context into account from all the training data, and tracks relationships in sequential data, like the words in a sentence, to develop some understanding of the real world.

At **inference** time, the input text is tokenized into individual tokens which are fed into the model. After processing using the transformer mechanism, the model returns result tokens which are then turned back into readable text.

## Use cases

We can group the Generative AI use cases in the following different categories:

### Improve customer experiences

* Chatbot functionality with context with better user experience than earlier technologies. 
* Reduces operational costs using automated responses.
* Documentation summarization: See models like Jurassic-2 Jumbo from [AI21 studio](https://www.ai21.com/studio).  Anthropic's `claude-v2` works well too.
* Personalization

### Improve employee productivity

* Code generation
* Translation, reports, summarization...
* Search via Q&A Agent for specific subjects, based on enterprise document processing. The LLM helps understanding the text and the questions. The LLM is enriched and trained on a proprietary corpus:

    ![RAG chatbot](./diagrams/qa_llm.drawio.png){ width=600}

* Self service tutor based on student progress, prompt activities, and respond to questions
* Personalized learning path generation
* Low-code development with GenAI agents

### Creativity

* Auto-generation of marketing material
* Personalized emails
* Sales scripts for customer's industry or segment
* Speeding the ideation phase of a product development

### Business process optimization

* Automatically extract and summarize data from documents: combine OCR with prompt to extract data and build json doc to be structured for downstream processing: Gen AI based intelligent document processing may look like this:

    ![Document Processing Flow](./diagrams/idp_genai.drawio.png){ width=600}

* Data augmentation to improve data set quality. Keep the privacy of original data sources, and help trains other models: generate image of rusted pumps to train an anomaly detection model on pumps.
* Propose some supply chain scenario

## Retrieval Augmented Generation (RAG)

LLMs are trained at a specific moment in time, and therefore have a knowledge cut-off time, after which data are not directly available to the model.  When enterprises need their LLM-based applications to use private information, they can fine-tune models or insert semantic search results into the LLM's input context window. Retrieval Augmented Generation is an approach that addresses this problem by supplementing generative text models with data that it was not trained on but is discovered by examining the user's query and finding relevant additional information prior to calling the LLM.

### Basic architecture

The Retrieval Augmented Generation may be seen as a three stage process:

![RAG Stages](./diagrams/rag_3_stages.drawio.png){ width=900 }

1. **Indexing**: A batch process to ingest documents and data from a source and index them. During this process semantic search is used to retrieve relevant documents from the index. Indexing supports reading the documents and splitting large ones into smaller chunks. Chunks help to stay within the LLM's context window. Indexing includes storage of the documents and index the chunks.
1. **Retrieval**: Retrieves the relevant data (chunks) from the index, then pass that to the model as part of the context.
1. **Generation**: Generate the response in plain natural language.

This process is supported by tools for documents ingestion, splitting, embedding, indexing, retrieval and integration with the real time conversation flow.

RAG systems work well because LLMs has the in-context learning capability, which allows models to use previously unseen data to perform accurate predictions without weight training.

As LLM increase the context window size over new release, RAG can add more new data to it.

### RAG Challenges

Naive RAG has severe limitations which has limited large-scale adoption:

* It is hard to do reliable, scalable RAG on a large knowledge corpus.
* Limited to single-shot prompts.
* No query understanding, just a sematic search.
* No query decomposition for planning.
* No tool use to query an external data source to enrich the context.
* No reflection and error correction to improve the quality of the response.
* No persistence or memory of previous queries.

Therefore, while invaluable for enriching context, RAG often needs to be enhanced with other technologies and approaches for full-scale enterprise applications.

## Hybrid AI

Hybrid AI refers to the integration of different AI approaches or techniques to create more robust and capable AI systems. The classical hybrid AI is to combine traditional, rule-based **symbolic AI** systems with deep learning models. The rule-based engine can handle logical reasoning and knowledge representation, while the deep learning component handles pattern recognition and unstructured data processing.

In addition to rule-based systems, Hybrid AI solutions can also leverage other decision engines such as optimization engines, knowledge graphs, or synbolic planning engines for specialized domain-specific applications.   In addition, all of these can be enhanced with specialized machine learning models to provide additional contextual information about historical patterns and scores.

Another architecture for hybrid AI a multi-agent system, which combines multiple specialized AI agents, each with their own capabilities and decision-making processes, to tackle complex problems that require diverse skills and perspectives. These agents can be chained together or deployed for parallel processing. Agents are stateful.

Here is a typical example of a hybrid AI architecture:

![Hybrid AI Architecture](./diagrams/hybrid_ai_comp.drawio.png){ width=900 }

The backend for a chatbot includes assistants that organize an agent workflow, that integrates LLMs, classical machine learning predictive scoring models, knowledge graphs, rule-based engines, and vector stores for similarity searches. Such an agent workflow is stateful.

### Why Use Hybrid AI?

Hybrid systems can achieve better overall accuracy than a generic LLM; they are more resilient to the weaknesses or limitations of LLMs.  They are grounded, precise, transparent, and more amenable to meaningful explanations of their behavior and decisions.  They can take into account up-to-date data from documents and data within the enterprise. The use of knowledge graph and rule-based systems make the AI architecture more flexible to support a wider range of problems and scenarios.

When an enterprise must demonstrate compliance and follow specific policies and regulations, symbolic AI results are more interpretable and explainable than neural network decisions.  This is critical both for good organizational behavior and for audits.

### Hybrid AI Conclusion

Of course, leveraging multiple technologies comes at a cost:  The architecture, development, and governance costs of maintaining such a solution is significant.   Typically symbolic engine solutions must be hand-coded (for example, business rules must be discovered, authored, tested, and deployed).   Machine learning models must be trained on large amounts of data.   RAG systems depend on a curated and processed corpus of documents.

All of this is real work that requires people with skills and experience.   Tools exist and are being enhanced all the time to simplify the process of creating and maintaining these components, but enterprises should go into these projects with their eyes open to avoid frustration and disappointment.    AI can produce great results - but it's not magic.   Our recommendation:  work with people experienced not only the latest AI technologies, but in created real, deployed, enterprise systems, and people who have experience with the full breadth of tools that can be brought to bear to create a meaningful solution for your business.

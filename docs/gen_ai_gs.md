# Getting Started in Generative AI

## Introduction

Generative AI is a combination of neural network models to create new content (text, image, music, videos..) from a requesting query. Models are pre-trained on vast amounts of unlabeled data, using from 7B up to 500B of parameters. The models are trained on vast amounts (Terabytes) of text data like books, articles, websites etc. his helps the model learn grammar, facts, reasoning abilities and even some level of common sense from the content.

Gen AI applies well to different category of use cases: improve customer experiences, improve employee's productivity, help around creativity, and help optimizing business process.

### Transformer Architecture

**GPT-3 (Generative Pre-trained Transformer 3)** breaks the NLP boundaries with training on 175B parameters. It is built on **Transformer** which uses self-**attention** mechanism to weigh the significance of different words in a sentence to understand the context in a sequence of data. 

To process a text input with a transformer model, the text is **tokenized** into a sequence of words or part of words. These tokens are then **encoded** as numbers and converted into **embeddings**, which are vector-space representations of the tokens that preserve their meaning. Next, the encoder in the transformer, transforms the embeddings of all the tokens into a **context vector**. Using this vector, the transformer decoder generates output based on clues. The decoder can produce the subsequent word. This process can be repeated to create an entire paragraph. This process is called **auto-regressive generation**.

The **attention** mechanism computes the similarity between tokens (the embeddings of words) in a sequence. The process keeps few tokens around each word to help understand the context. This surrounding group of tokens is called the **context window**. It is the sliding group of tokens around a word that provides contextual information. That way, the model builds an intuition of what the text is saying. The closer two words are in a vector space, the higher the attention scores they will obtain and the higher the attention they will give to each other.

The second part of the GPT-3 architecture are the **layers** of transformers stacked on top of each other. Within each layer, there are feed-forward neural networks to process the data.

The training has two stages: **Pre-training** where the model attempts to predict the next word in a sentence using its own corpus, and **fine tuning** where the model can be tuned for specific *tasks* or *content*. During the pre-training process, the model automatically takes context into account from all the training data, and tracks relationships in sequential data, like the words in a sentence, to develop some understanding of the real world.

At **inference** time, the input text is tokenized into individual tokens which are fed into the model. After processing using the transformer mechanism, the model returns result tokens which are then turned back into readable text.

## Use cases

We can group the Generative AI use cases in different categories:

???- info "Improve customer experiences"
    * Chatbot functionality with context, with better user's experiences. Reduce operational costs using automated response.
    * Documentation summarization: See model like Jurassic-2 Jumbo from [AI21 studio](https://www.ai21.com/studio), claude-v2 works well too.
    * Personalization


???- info "Improve employee productivity"
    * Code generation
    * Translation, reports, summarization...
    * Search via Q&A Agent for specific subject, based on Corporate document processing. LLM helps understanding the text and the questions. The LLM is enriched, trained on proprietary corpus:

    ![](./diagrams/qa-llm.drawio.png){ width=400}

    * Self service tutor based on student progress, prompt activities, and respond to questions
    * Personalized learning path generation
    * Low-code development with GenAI agents

???- info "Creativity"
    * Auto-generation of marketing material
    * Personalized emails
    * Sales scripts for customer's industry or segment
    * Speeding the ideation phase of a product development

???- info "Business process optimization"
    * Automatically extracting and summarizing data from documents: combine OCR with prompt to extract data and build json doc to be structured for downstream processing: Gen AI based intelligent document processing may looks like this:

    ![](./diagrams/idp-genai.drawio.png)

    * Data augmentation to improve data set quality. Keep the privacy of original data sources, and help trains other models: generate image of rusted pumps to train an anomaly detection model on pumps.
    * Propose some supply chain scenario

## Challenges

First of all the current level of model accuracy should not be acceptable to any enterprise under regulations and with customer centric strategy. Models produce incorrect and contradictory answers. With classical ML, output is well expected. Trained sentiment analysis algorithms on labelled data will perform better than any LLM for that task. Always try to assess when to use ML.

A single large model is unlikely to solve every business problem effectively. To differentiate their generative AI applications and achieve optimal performance, companies should rely on their **own data sets** tailored to their unique use case. Cost of training and inference, privacy and intellectual property are top concerns. FM can be "fine-tuned" for a specific task, by using a small number of labeled examples, specific to the company's industry or use case. Fine-tuned models can deliver more accurate and relevant outputs. But training, retraining model and even inference are expensive.

Reinforcement learning to fine-tune existing LLM require a very important amount of trials.

Generative AI models could not reason and plan. 

## Retrieval Augmented Generation (RAG)

LLMs have a knowledge cut-off time, where data coming after are not known by the model.  Pre-training is a one-off exercise. When enterprises need to get their private knowledge integrated to LLM, they can do fine tuning or present semantic search results as part of the input context window. Retrieval Augmented Generation addresses this problem as it is the act of supplementing generative text models with data outside of what it was trained on.

### Basic architecture

The Retrieval Augmented Generation may be seen as a three stages process:

![](./diagrams/rag_3_stages.drawio.png)

1. **Indexing** a batch processing to ingest documents and data from a source and indexing them. During processing semantic search is used to retrieve relevant documents from the index. Indexing supports loading the documents, splitting large documents into smaller chunks. Chunks help to stay within the LLM's context window. Indexing includes storage of the documents and index of the splits.
1. **Retrieval**: retrieves the relevant data (splits) from the index, then passes that to the model as part of the context.
1. **Generation**: generate the response in plain natural language.

This process is supported by tools for documents ingestion, splitting, embedding, indexing, retrieval and integration with the real time conversation flow.

RAG systems work well because LLMs has the in-context learning capability, which allows models to use previously unseen data to perform accurate predictions without weight training.

As LLM increase the context window size over new release, RAG can add more new data to it. 

### Challenges

Naive RAG has very important limitations which has generated some adoption challenges:

* It is hard to do a reliable, scalable RAG on a large knowledge corpus
* Limited to single-shot prompt
* No query understanding, just a sematic search
* No query decomposition for planning
* No tool use, to query an external data source to enrich the context
* No reflection and error correction to improve the quality of the response.
* No persistence or memory of previous queries
# Owl Agent Backend Design

For modifying and enhancing the OwlAgent Framework backend, the code is in [athena-owl-core/owl-agent-backend](https://github.com/AthenaDecisionSystems/athena-owl-core/tree/main/owl-agent-backend). This chapter explains the code and implementation approach, and then how to continue developing and testing the backend.

## The core concepts

The core concepts the framework manages are assistants, agents, tools, and prompts.  Here is a how they are related:

![](./diagrams/design/owl_entities.drawio.png){ width=900 }

An *Assistant* supports a specific business use case, like helping a worker in a specific task of a business process, which may involve the coordination of multiple agents. Assistants may be stateful to keep state of the conversation with snapshot capabilities.

An *Agent* is a grouping of Large Language Model or fine tuned smaller Language Models, each with a prompt and tools, to accomplish a subtask of the assistant. A *retriever* is a tool to access a collection or document within a vector store. So using RAG means using a retriever. 

## Code organization

The code for the backend is in the `src` folder, while unit tests and integration tests are under `tests/ut/` and `tests/it`.

The main entry point for the owl-backend is the [athena.main.py](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/athena/main.py) which is a FastAPI server.

The backend can run in uvicorn or ugnicorn server. It exposes two set of APIs: 

* `/api/v1/c/` for the conversation with chatbot user interface
* `/api/v1/a/` for the administration tasks, such as managing the different OWL entities of the frameworks: assistants, agents, prompts, tools, RAG documents...

The `src` folder includes the Dockerfile to build the image, the `requirements.txt` is used for Python module dependencies and a `start_backend.sh` script to do local development tests. Unit and integration test are done using `pytest` and unittest modules. Code testing can be debugged in VScode IDE.

## Important components

The [architecture document presents the components](arch.md/#component-view). The decomposition is done with API, service/repository code and then llm specific facade code.

![](./images/design/code_repo.PNG)

| Folder | Functions |
| --- | --- |
| **routers** | Includes the different REST resources: conversation, assistant, agent, tool, prompt and document |
| **config** | Configuration file when the application runs in container. The configuration files are mounted inside the container under /app |
| **itg** | This is for the integration, so most of the code there is mockup placeholder for demonstration, the only important component is the store to keep data about the files uploaded in the context of RAG |
| **llm** | The different repository to manage each OwlEntities like, assistant, agent, tools, prompts...There are also some pre-defined assistants and agents that could be used for integrating in solution |


### Conversation

The conversation API is in [routers/conversations.py](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/athena/routers/conversations.py). 

![](./diagrams/design/conversation_mgr.drawio.png)

The conversation manager [conversation_mgr.py](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/athena/llm/conversations/conversation_mgr.py) under `llm/conversations` folder exposes a factory method to create, or get from the cache, the assistant supporting the conversation. 
When an assistant is not in the memory, the factory delegates to the assistant manager the creation of the assistant.

Conversation uses a ConversationControl bean class. The definitions of those classes are in a DTO model so it can be easily shared with other app.

From the user interface the end user may select another assistant, and in this case a new thread should be started. When assistant uses implementation with Stateful capability, like in LangGraph, then the conversation will be saved as part of the memory management of LangGraph using the thread unique identifier.

Here is an example of a simple query to the LLM Anthropic Claude using an assistant that has Tavily search tool. The payload to the POST url is

```json
{
 
  "query": "What does the Athena Decision Systems company do?",
  "user_id": "jerome",
  "assistant_id": "base_tool_assistant",
  "thread_id": "1"
}
```

From a conversation interaction the sequence flow looks like in the following sequence diagram:

![](./diagrams/design/conv_seq_flow.drawio.png)

The Assistant and Agent are instance created by different factory taking into account the yaml definition of the matching Entity.

### Assistant

The Assistant manager is in [llm/assistants](https://github.com/AthenaDecisionSystems/athena-owl-core/tree/main/owl-agent-backend/src/athena/llm/assistants) folder. The current implementation uses the local file to persist assistant entity definitions. The assistant manager exposes a factory method to create assistant executor using the AssistantEntity information.

![](./diagrams/assistant_mgr_class.drawio.png)

See the validation unit test in [tests/ut/test_assistant_mg.py](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/tests/ut/test_assistant_mg.py) and the integration tests  [tests/it/test_assistants_api.py]

The `llm/assistants` folder includes some pre-defined assistant implementations:

| Assistant | Description |
| --- | --- |
| BaseAssistant | A default assistant to do simple LLM calls |
| Default tool assistant | Default tool assistant |
| Claude 3 with tool assistant | | 

While the configuration of the assistants are in the [config/assistants.yaml](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/athena/config/assistants.yaml) files

```yaml
base_tool_assistant:
  assistant_id: base_tool_assistant
  class_name: athena.llm.assistants.BaseToolAssistant.BaseToolAssistant
  description: A default assistant that uses LLM and search tool to do web search
  name: Default tool assistant
  agent_id: open_ai_tool
```

We can have multiple different assistant definitions for the same assistant implementation class.

The Assistant implementation can be a Langchain chain or a langGraph graph. Each assistant needs to implement the send_conversation and streaming methods.

```python
def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
```

### Agents

The Agent manager is in [llm/agents](https://github.com/AthenaDecisionSystems/athena-owl-core/tree/main/owl-agent-backend/src/athena/llm/agents) folder. The current implementation uses the local file to keep AgentEntity definitions. The agent manager exposes a factory method to create agent executor using the AgentEntity information.

![](./diagrams/agent_mgr_class.drawio.png)

Example of AgentEntity

```yaml
open_ai_tool:
  agent_id: open_ai_tool
  name: open_ai_gpt35
  description: openai based agent with prompt coming from langchain hub and tool
  class_name: athena.llm.agents.tool_agent_openai.OpenAIToolAgent
  modelName: gpt-3.5-turbo-0125
  prompt_ref: hwchase17/openai-functions-agent
  temperature: 0
  top_k: 1
  top_p: 1
  tools:
  - tavily
```

The validation unit tests are in [tests/ut/test_agent_mg.py](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/tests/ut/test_agent_mg.py) and the integration tests  in [tests/it/test_agents_api.py](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/tests/it)

The `llm/agents` folder includes some pre-defined agents:

| Agent | Description |
| --- | --- |
| Fake Agent | To do unit testing without cost |
| openai_chain |  openai based agent with simple prompt |
| Open_ai_tool | openai based agent with prompt coming from langchain hub  and tool |
| Agent anthropic with tools | Claude 3 with tool calling |

The configuration of the agents are in the [config/agents.yaml](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/athena/config/agents.yaml) files

### Tools

The concept of tools / functions was introduced by OpenAI, and most big LLM are supporting it now. 

Here is an example of python function that will be used as a tool:

```python
def query_crm_backend(query: str):
    """Call the customer relationship management (CRM) to get customer data."""

    return ["The customer records from DEMO CRM"]
```

An example of this function is in [demo_tools.py](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/athena/llm/tools/demo_tools.py)

The OWL Framework needs an implementation of a tool factory to be able to create tool references used by LLM API. 

???+ info "Langchain tool api"
    The classical way to add tools to a "LLM" instance in LangChain, is to define an AgentExecutor, which is a LLM and a prompt with the tools names.

    ```python
    agent = LLMSingleActionAgent(llm_chain=llm_chain, output_parser=output_parser,
        stop=["\nObservation:"], allowed_tools=tool_names,
    )
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools)
    ```

    The tool_names is a list of strings of the name of the tools, while the tools is a list of python functions matching the names.

    Zooming to the Prompt, it needs to include placeholders for tools and tool_names:

    **Answer the following questions as best you can, but speaking as a pirate might speak. You have access to the following tools:**

    **{tools}**

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of **[{tool_names}]**
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    Question: **{input}** \n    **{agent_scratchpad}**


Therefore the same python module needs to implement the tool factory class:

```python
from athena.llm.tools.tool_factory import ToolInstanceFactoryInterface
class DemoToolInstanceFactory(ToolInstanceFactoryInterface):
  def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
```

This factory uses LangChain to build StructuredTool:

```python
def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
    """ From the list of tools to use build the function reference for LLM """
    tool_list=[]
    for tool_entity in tool_entities:
        tool_list.append(self.define_tool( tool_entity.tool_description, tool_entity.tool_fct_name, tool_entity.tool_arg_schema_class))
    return tool_list
```

The tools.yaml includes the definition of the tool as a OwlEntity

```
query_crm:
  tool_id: query_crm
  tool_class_name: athena.llm.tools.demo_tools
  tool_description: """Call the customer relationship management (CRM) to get customer data."""
  tool_fct_name: 'query_crm_backend' 
```

When creating the agent, the tool definitions are loaded and then passed to the `build_tool_instances()` function. See [the code]()

### Document management

When a user uploads a document using the chatbot interface, the file is persisted in cloud object storage with some metadata. The file is parsed in sub-documents that vectorized via Embeddings. The created vectors are saved in a vector store. The [architecture section](./arch.md/#agent-manager) introduced the processing.

The REST resource is in the [document.py file](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/athena/routers/documents.py). It offers two APIs, one for the similarity search and one to upload the document. The filedrescription represent the metadata and myFile the binary stream coming from the client application.

```python
@router.post("/documents/")
async def post_document_for_rag( file_description: FileDescription = Depends(), myFile: UploadFile = File(...)):
    # it delegate to the document manager
```

The document manager is in the [itg/store/content_mgr.py](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/athena/itg/store/content_mgr.py) file. The logic to process the uploaded file is:

1. Persist the metadata file and potentially the file content itself in the storage uri as specified in config.yaml file: `owl_agent_content_file_path`
1. From the document type, perform the different chunking and embedding, as the tool to parse and split the main document are different.
1. Create embeddings and save them in vector store in the collection as defined by the config file

The content_mgr offers a `get_retriever()` method to be using in LLM RAG implementation.

## Running locally

### Pre-requisites

* Prepare your .env file, using your personal Keys

```yaml
OPENAI_API_KEY=---your-key---
WATSONX_APIKEY=---your-key---
MISTRAL_API_KEY=---your-key---
LANGCHAIN_API_KEY=---your-key---
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
...
```

* Create and start virtual python env (once created just activate it). Test with python 3.12.3. Above that there is some incompatibility with langchain modules (as of 6/15/2024).

```sh
python -m venv .venv
# for MAC / Linux users
source ./venv/bin/activate
# for Windows
source ./venv/Scripts/activate
```

* Install the needed python modules with `pip install -r src/requirements.txt` and `pip install -r tests/requirements.txt`
* build the owl backend image under the `owl-agent-backend` folder.

```sh
./build/buildImage.sh
```

This image can be pushed to docker hub. (as of now it is the `jbcodeforce/athena-owl-backend:latest` image)

![](./images/docker-hub.PNG)

* Build the owl-frontend docker image under the `owl-agent-frontend` folder:

```sh
./build/buildImage.sh
```


### Development mode

While developing the backend, the approach is to use test-driven development and start by writing unit tests for any new or changed feature. Each unit test python file defines a `unittest.TestCase` class and a test method. For each entity manager, instantiate a manager and then do some testing of the api.

For conversations, use the ConversationControl object.

```python
def test_base_assistant_with_chat_history(self):    
    cc = ConversationControl()
    cc.assistant_id="base_assistant"
    cc.user_id="unit_test"
    cc.thread_id="1"
    cc.chat_history=[]
    cc.query="Hi, I'm Bob and my last name is TheBuilder."
    rep = get_or_start_conversation(cc)
    assert rep
    assert rep.message
```

It is also possible to start a uvicorn server with continuous upload of the code and then test using the OpenAI exposed.

1. Start the server under the `src` folder with `./start_backend.sh`. It uses a special config file (named [local-config.yaml](https://github.com/AthenaDecisionSystems/athena-owl-core/blob/main/owl-agent-backend/src/local-config.yaml)) to access the other entities configurations.
1. Use the [localhost:8000/docs](http://localhost:8000/docs) URL
1. Use any of the entity APIs
1. Use the generic/chat URL to send the conversation.

The minimum payload to use one of the assistant is the following:

```json
{
  "query": "What is Athena Decision Systems all about?",
  "user_id": "jerome",
  "assistant_id": "fake_assistant",
  "thread_id": "1"
}
```

### Run unit tests

Running all the tests for non-regression validation:

```sh
pytest -s tests/ut/
```

To debug unit tests in VSCode:

* As the src code and tests are in separate folders, be sure to have configured the debugger launch settings as:

```json
{
    "version": "0.2.0",
    "configurations": [
        
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": { "PYTHONPATH": "${workspaceRoot}/owl-agent-backend/src"},
            "cwd": "${workspaceRoot}/owl-agent-backend"
        }
    ]
}
```

Then breakpoint and step by step.

![](./images/debug_ut.PNG)

### Integration mode

There are two ways to do integration tests, with docker or with the start_backend.sh script.



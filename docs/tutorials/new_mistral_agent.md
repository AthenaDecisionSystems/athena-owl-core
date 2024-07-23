# Developing a new agent based on Mistral

In this tutorial, you will learn how to develop a new agent for the Mistral API and integrate it into an existing Assistant. The end game code we will be developing can be found in `llm/agents/mistral_agent.py` and the config file.

The following diagram illustrates what is built:

![New Agent Overview](./diagrams/new_agent.drawio.png)

## Pre-requisites

You need to get a `MISTRAL_API_KEY` from [mistral.ai](https://mistral.ai). Be sure to get a little familiar with their API [using their getting started guide.](https://docs.mistral.ai/getting-started/quickstart/)

Update the `.env` file in the backend with the `MISTRAL_API_KEY` environment variable.

You need to set up your development environment [according to this note](./dev_env.md)

## Defining The Agent

An agent defines at a minimum the LLM API client code, a model reference and parameters, and how to manage a conversation. A new agent has a contract with the OwlAgent Framework via the OwlAgent class. Therefore the first step is to create an agent Python file named `mistral_agent.py` and define a class that supports the contract of the constructor as shown below:

```py title="llm/agents/mistral_agent.py"
from athena.llm.agents.agent_mgr import OwlAgentInterface,

class MistralAgent(OwlAgentInterface):
    
    def __init__(self,agentEntity: OwlAgentEntity, prompt: BasePromptTemplate, tool_instances: Optional[list[Any]]):
        self.prompt = prompt
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
```

Since we are good test-driven developers, let's start by writing unit tests for this class: Under the `tests/ut` folder add a Python file called `test_mistral_agent.py` by copying the unit test template:

```sh
# under tests/ut
cp template_ut.py test_mistral_agent.py
```

Rename the class and add a first test:

```py title="tests/ut/test_mistral_agent.py"
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgentEntity

class TestMistral(unittest.TestCase):

    def test_define_agent_entity_create_instance(self):
        """
        From the OwlAgentEntity verify the factory can create the agent executor
        """
        print("\n\n >>> test_define_agent_entity_create_instance\n")
        agent_entity = OwlAgentEntity(agent_id="mistral_large",
                                      modelName="mistral-large-latest",
                                      modelClassName="langchain_mistralai.chat_models.ChatMistralAI",
                                      temperature=0,
                                      )
        assert agent_entity
        mgr = get_agent_manager()
        agent_executor = mgr.build_agent_from_entity(agent_entity)

```

Running this test with `pytest -s tests/ut/test_mistral_agent.py` may fail as the `langchain-mistralai` is missing in the `src/requirements.txt`. You can fix that by adding it explicitly and doing `pip install langchain-mistral`.  Once done the test should be able to create an agent instance.

## Adding a system prompt

A system prompt is a text instruction to the LLM that says what is required so it can better answer the user's query. Taking the example from Mistral site, you will define a RAG system prompt which takes into account existing context.

* Add a yaml definition within the `tests/ut/config/prompts.yaml` file:

```yaml title="tests/ut/config/prompts.yaml"
mistral_rag_prompt:
    name: Mistral Bank Query Classification
    prompt_id: mistral_rag_prompt
    locales:
    - locale: en
    text: |
        "Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}"
```

For unit testing, the configuration of the Owl framework is defined in `./tests/ut/config/config.yaml` and set up in each test class using the environment variable `CONFIG_FILE`.

Add a unit test to validate that the prompt is correctly loaded:

```py title="tests/ut/test_mistral_agent.py"
def test_valide_prompt_is_loaded(self):
    prompt_mgr = get_prompt_manager()
    mistral_prompt = prompt_mgr.get_prompt("mistral_rag_prompt")
    assert mistral_prompt    # this is a string
    print(pe)
```

Add the prompt reference to the OwlAgentEntity

```py title="add prompt to test_mistral_agent.py"
agent_entity = OwlAgentEntity(agent_id="mistral_large",
                                name="Mistral based agent",
                                class_name="athena.llm.agents.mistral_agent.MistralAgent",
                                modelName="mistral-large-latest",
                                prompt_ref="mistral_rag_prompt",   
)
```

For the snippet above:  The reference needs to match the `prompt_id`.

Rerunning the unit test should succeed, but we are not yet calling the LLM. The next step is to create a LangChain chain and then do a simple invocation.

## Adding A Chain

To add a chain to the agent, add the following code:

```py title="Update constructor in mistral_agent.py"
    def __init__(self,agentEntity: OwlAgentEntity, prompt: BasePromptTemplate, tool_instances: Optional[list[Any]]):
        self.prompt = prompt
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
        self.llm = self.prompt | self.model | StrOutputParser()   # (1)
    
    
    def get_runnable(self):
        return  self.llm  # (1)
```

The lines marked `(1)` are newly added.

The prompt has defined a new variable called `context`. The OwlFramework defines the following prompt template from the system prompt text:

```py title="prompt builder function in prompt_mgr.py"
 ChatPromptTemplate.from_messages([
            ("system", text),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ])
        
```

The `chat_history` and `agent_scratchpad` variables are optional, but not the `input`. So you need to add some parameters to the test:

```py title="add invocation to test_mistral_agent.py"
    assert agent_executor
    rep = agent_executor.invoke({"input" : "What is langgraph?", "context": ""})
    print(rep)
```

The invocation to Mistral should work but respond something like the following answer: _"I'm sorry for the confusion, but the context provided is empty, and I don't have any information about "langgraph" from the given context."_

At this stage we have a running (albeit not particularly useful) agent, but one that can be a component for building a useful assistant that can call Mistral.

## Define a New Assistant

The OwlAgent Framework has some predefined agents. In the new assistant you will use the LangGraph flow for two nodes, the call to LLM and the tool node.

The first operation is to add the new agent in `src/athena/config/agents.yaml`

```yaml title="src/athena/config/agents.yaml"
mistral_large:
  agent_id: mistral_large
  class_name: athena.llm.agents.mistral_agent.MistralAgent
  description: A Mistral large agent for RAG question and answer
  modelClassName: langchain_mistralai.chat_models.ChatMistralAI
  modelName: mistral-large-latest
  name: Mistral based agent
  prompt_ref: mistral_rag_prompt
  temperature: 0
  tools: []
  top_k: 1
```

Then create an assistant that uses this agent:

```yaml title="src/athena/config/assistants.yaml"
mistral_tool_assistant:
  assistant_id: mistral_tool_assistant
  class_name: athena.llm.assistants.BaseToolGraphAssistant.BaseToolGraphAssistant
  description: A default assistant that uses Mistral
  name: Mistral large with tool assitant
  agents: 
    - mistral_large

```

Now let's add a test for the assistant. For that, add a new test function:

```py title="add test at the API to trigger assistant execution to test_mistral_agent.py"
from athena.routers.dto_models import ConversationControl
from athena.main import app
from athena.app_settings import  get_config
from fastapi.testclient import TestClient

def test_mistral_assistant_with_mistral_agent(self):
        print("\n\n >>> test_mistral_assistant_with_mistral_agent at the API level\n")
        client = TestClient(app)
        ctl = ConversationControl()
        ctl.assistant_id="mistral_tool_assistant"
        ctl.user_id="test_user"
        ctl.thread_id="1"
        ctl.query="What is Athena Owl Agent?"
        response=client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"\n---> {response.content}")
```

The test should fail because we have missing tools.

## Adding tools to retrieve documents from a corpus

_JB to continue..._
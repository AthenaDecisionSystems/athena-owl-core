# Build solution

Developing a new solution should be simple, but complexity is linked to the level of integration needed, as usual. 

To get started consider the scope of the demonstration and assess if you need to:

- Use a specific LLM backend
- Have an existing decision service available or if you need to develop a new one. A new decision service means new rules but also a new execution model.

## Develop your own demonstration

### Define Assistant

Add the following base declaration for the main Assistant of the solution. One Assistant per use case.

```yaml
ibu_assistant:
  assistant_id: ibu_assistant
  class_name: athena.llm.assistants.BaseToolGraphAssistant.BaseToolGraphAssistant
  description: A default assistant that uses LLM, and local defined tools like get borrower, and next best action
  name: IBU Loan App assistant
  agent_id: ibu_agent

```

The class name is coming from Owl Agent core library. This is the LangGraph flow with tool and LLM. The graph looks like in the following figure:

![](./diagrams/lg_tool_flow.drawio.pngs)

### Define Agent

### Define Tools

The classical common integration is when the solution needs to get data from an existing database or better a microservice managing a specific business entity. In this case the solution leverage a python function that can remote call the microservice URL using library like `requests`.

For short demonstration you may need to implement some mockup repository that could be integrated into the demo run time.

#### Adding a function as tool

OpenAI has started the initiative of function calling and now most of the major proprietary or open source LLM model supports tool calling. As Owl Agent is using LangGraph for agent orchestration, we will use LangChain tools API to define function calling.

There are [three ways](https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/) to do so with LangChain: function annotation, using a factory function or class sub-classing. 

The tool annotation is the simplest approach. The following declaration uses annotation, and the argument names, type and comment description are very important as they will be injected as context in the prompt to the LLM. Be sure to be short but brings semantic so the LLM can decide to call the function to get more information about a client, and being able to extract the first and last names from the query message.

```python
@tool
def get_client_by_name(first_name: str, last_name: str) -> str | None:
    """get borrower client information given his or her name"""
    return build_or_get_loan_client_repo().get_client_by_name_json(first_name,last_name)

```

#### Adding a mockup repository 

Define an interface for the repository with only the methods used in the solution:

```python
class LoanApplicationClientRepositoryInterface:

    def get_client_by_name(self,first_name: str, last_name: str) -> Borrower | None:
        return None
    
    
    def get_client_by_name_json(self,first_name: str, last_name: str) -> str | None:
        return None

```

Then implement the mockup repository with your test data.

### Define prompt

### Integration tests

### Custom user interface
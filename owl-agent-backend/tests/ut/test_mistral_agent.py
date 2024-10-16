import unittest
import sys
import os
import yaml
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from dotenv import load_dotenv
load_dotenv()


from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgent, OwlAgentDefaultRunner
from athena.llm.tools.tool_mgr import OwlToolEntity
from athena.llm.tools.demo_tools import DemoToolInstanceFactory, CrmArgument, CustomerClassEnum
from athena.llm.prompts.prompt_mgr import get_prompt_manager
from langchain_core.prompts import ChatPromptTemplate,  MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage



class TestMistral(unittest.TestCase):
    
    def setUp(self):
        self.agent_entity = OwlAgent(agent_id="mistral_large",
                                      name="Mistral based agent",
                                      runner_class_name="athena.llm.agents.agent_mgr.OwlAgentDefaultRunner",
                                      modelName="mistral-large-latest",
                                      prompt_ref="mistral_rag_prompt",
                                      modelClassName="langchain_mistralai.chat_models.ChatMistralAI",
                                      temperature=0,
                                      )

    def test_yaml_view(self):
        print("\n\n >>> test_yaml_view\n")
        oae_dict = self.agent_entity.model_dump()
        oaes= {}
        oaes[self.agent_entity.agent_id]=oae_dict
        oaes_yaml_str=yaml.dump(oaes)
        print(oaes_yaml_str)

    def test_valide_prompt_is_loaded(self):
        print("\n\n >>> test_valide_prompt_is_loaded\n")
        prompt_mgr= get_prompt_manager()
        mistral_prompt = prompt_mgr.get_prompt("mistral_rag_prompt")
        assert mistral_prompt    # this is the text of the system prompt
        print(mistral_prompt)



    def test_from_agent_entity_create_runner_instance(self):
        """
        From the OwlAgent verify the factory can create the agent executor
        """
        print("\n\n >>> test_define_agent_entity_create_instance\n")
        print(self.agent_entity)
        mgr=get_agent_manager()
        agent_executor: OwlAgentDefaultRunner =mgr.build_agent_runner_from_entity(self.agent_entity)
        assert agent_executor
        rep = agent_executor.invoke({ "input": ["What is langgraph?"], 
                                     "chat_history": [], 
                                     "context": ["LangGraph is a python library from langchain team."]}, "test_thread")
        print(rep)
        assert rep

    def test_crm_argument(self):
        print("\n\n >>> test_crm_argument\n")
        crm_arg = CrmArgument(user_id="U01", customer_class=CustomerClassEnum.media, customer_id="C01", query="MediaIncTheGroup")
        json_arg: str = crm_arg.json()
        assert "U01" in json_arg
        
        
    def _test_define_demo_tool_and_agent(self):
        """Test using lower api to create tool entity by code to unit test tool"""
        print("\n\n >>> test_define_demo_tool_and_agent\n")
        query_crm_tool_entity: OwlToolEntity = OwlToolEntity(tool_id= "query_crm",
                                                tool_class_name= "athena.llm.tools.demo_tools",
                                                tool_description= "Call the customer relationship management (CRM) to get customer data using the CrmArgument json",
                                                tool_fct_name= "query_crm_backend",
                                                tool_arg_schema_class="CrmArgument")
        tool_instances = DemoToolInstanceFactory().build_tool_instances([query_crm_tool_entity])
        prompt= ChatPromptTemplate.from_messages([
                        ("system", """
                        You are helpful assistant for customer management and query. 
                         Assistant can ask the user to use tools to look up information that may be helpful in \
            answering the users original question. The tools the human can use are:

            {tools}

            RESPONSE FORMAT INSTRUCTIONS
            ----------------------------

            When responding to me, please output a response in one of two formats:

            **Option 1:**
            Use this if you want the human to use a tool.
            Markdown code snippet formatted in the following schema:

            ```json
            {{
                "action": string, \\ The action to take. Must be one of {tool_names}
                "action_input": string \\ The input to the action
            }}
            ```

            **Option #2:**
            Use this if you want to respond directly to the human. Markdown code snippet formatted \
            in the following schema:

            ```json
            {{
                "action": "Final Answer",
                "action_input": string \\ You should put what you want to return to use here
            }}
            ```
                        Using the given tool definitions select the appropriate tools to answer user query
                        """),
                        MessagesPlaceholder(variable_name="chat_history", optional=True),
                        ("human", "{input}"),
                        MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
                ])

        agent_executor: OwlAgentDefaultRunner =OwlAgentDefaultRunner(self.agent_entity, prompt, tool_instances)    
        assert agent_executor
        rep=agent_executor.invoke({ "input": ["my user_id is j9r, I want to get the last meeting records for the customer: C01, in the retail customer class"], 
                                   "chat_history": [],
                                    "context": []}, "test_thread")
        print(type(rep))
        print(rep)
        assert rep
        
    def test_parsing_response(self):
        rep = AIMessage(content='', 
               additional_kwargs={'tool_calls': [{'id': 'MpNBdjkiY', 'function': {'name': 'query_crm_backend', 'arguments': '{"query": "get_last_meeting_records_for_customer C01"}'}}]},
               response_metadata={'token_usage': {'prompt_tokens': 89, 'total_tokens': 127, 'completion_tokens': 38}, 'model': 'mistral-large-latest', 'finish_reason': 'tool_calls'},
               id='run-af9c2379-f6a0-4896-9d58-22387536ffd8-0',
               tool_calls=[{'name': 'query_crm_backend', 'args': {'query': 'get_last_meeting_records_for_customer C01'}, 'id': 'MpNBdjkiY'}],
               usage_metadata={'input_tokens': 89, 'output_tokens': 38, 'total_tokens': 127})
        # When tool call the content is empty
        assert len(rep.content) == 0
        tool=rep.tool_calls[0]
        assert tool
        print(tool["name"])
        print(tool["args"])
        
        
if __name__ == '__main__':
    unittest.main()
    
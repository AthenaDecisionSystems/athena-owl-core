import unittest, sys, os
from dotenv import load_dotenv
load_dotenv()
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
import yaml,json
from typing import Optional 
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgent
from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestAgentsManager(unittest.TestCase):
    """
    Validate CRUD on agent entity and factory of agent instance
    """
    def test_owl_agent_entity_to_json_to_yaml(self):
        print("\n\n >>> test_owl_agent_entity_to_json_to_yaml\n")
        # Use the default setting of the OwlAgent
        oae = OwlAgent()
        oae.agent_id="a_nice_agent"
        oae_dict = oae.model_dump()
        assert oae_dict["runner_class_name"] == "athena.llm.agents.agent_mgr.OwlAgentAbstractRunner"
        oaes= {}
        oaes[oae.agent_id]=oae_dict
        oaes_json_str=json.dumps(oaes)
        assert "OwlAgentAbstractRunner" in oaes_json_str
        # to map to a yaml
        oaes_yaml_str=yaml.dump(json.dumps(oaes))
        print(oaes_yaml_str)
        assert isinstance(oaes_yaml_str,(str))
        yaml_str=yaml.dump(oaes)
        print(f"Yaml view:\n {yaml_str}\n")
 
        
    def test_create_get_by_id_delete_agent_entity(self):
        print("\n\n >>> test_create_get_by_id_delete_agent_entity\n")
        oae = OwlAgent()
        oae.name="test_agent"
        oae.description="an openai based agent"
        mgr = get_agent_manager()
        oad_id=mgr.save_agent(oae)
        assert oad_id
        oa2 = mgr.get_agent_by_id(oad_id)
        assert oa2
        assert "openai" in oa2.description
        assert "test_agent" in oa2.name
        rep = mgr.delete_agent(oad_id)
        assert "Done" == rep
    
    def test_get_all_predefined_agents(self):
        print("\n\n >>> test_get_all_predefined_agents\n")
        mgr = get_agent_manager()
        l = mgr.get_agents()
        assert l
        assert len(l) >= 2
    
    def test_get_agent_by_name(self):
        # Should get the default agent definition
        print("\n\n >>> test_get_agent_by_name\n")
        mgr=get_agent_manager()
        assert mgr
        p=mgr.get_agent_by_name("OpenAI chain")
        assert p
        assert "OpenAI" in p.description
        
    def test_read_tool_list(self):
        print("\n\n >>> test_read_tool_list\n")
        mgr=get_agent_manager()
        p=mgr.get_agent_by_name("Claude-3 Opus")
        assert type(p) == OwlAgent
        assert len(p.tools) == 0 
        print(p)
    
    # ---------- now create agent runners -------------
    def test_calling_fake_agent(self):
        mgr = get_agent_manager()
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("fake_agent")
        if oae is None:
            raise ValueError("Fake agent not found")
        fake_agent = mgr.build_agent_runner(oae.agent_id,"en")
        assert fake_agent
        rep = fake_agent.invoke("what is langgraph?")
        assert "one" == rep
        rep = fake_agent.invoke("really?")
        assert "two" == rep
    
    def _validate_history(self, cc : ConversationControl):
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        
        print(f"\n\nagent --> {rep}") 
        
        cc.chat_history=rep.chat_history
        cc.query="What is my last name?"
        print(f"Continue the conversation with  --> {cc}") 
        rep = get_or_start_conversation(cc)
        print(f"\n\nAgent --> {rep}") 
        assert "last name is TheBuilder" in rep.message


    def test_calling_base_agent(self):
        print("\n\n test_calling_base_agent\n")
        mgr = get_agent_manager()
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("openai_tool_chain")
        if oae is None:
            raise ValueError("Base agent not found")
        base_agent =  mgr.build_agent_runner(oae.agent_id,"en")
        assert base_agent
        # Default agent has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = base_agent.send_conversation(cc)
        assert rep
        print(rep.messages[0].content)
        assert "LangGraph is a " in rep.messages[0].content

    def test_calling_base_graph_agent(self):
        print("\n\n test_calling_base_graph_agent\n")
        mgr = get_agent_manager()
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("openai_graph_agent")
        if oae is None:
            raise ValueError("Base agent not found")
        base_agent =  mgr.build_agent_runner(oae.agent_id,"en")
        assert base_agent
        # Default agent has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = base_agent.send_conversation(cc)
        assert rep
        print(rep.messages[0].content)  # should give wrong answer
        assert "LangGraph is a " in rep.messages[0].content

    def _test_long_conv_openai_base_graph_agent(self):
        # TO DO fix this test, it does not take the chat history well into account
        print("\n------- test_conv_openai_base_graph_agent")
        cc = ConversationControl()
        cc.agent_id="openai_graph_agent"
        cc.user_id="unit_test"
        cc.thread_id="3"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        self._validate_history(cc)

    def test_calling_base_tool_graph_agent(self):
        print("\n\n test_calling_base_tool_graph_agent \n")
        mgr = get_agent_manager()
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("base_tool_graph_agent")
        if oae is None:
            raise ValueError("agent not found")
        owl_agent =  mgr.build_agent_runner(oae.agent_id,"en")
        assert owl_agent
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = owl_agent.send_conversation(cc)
        assert rep.messages
        print(rep)
        trace = owl_agent.get_conversation_trace(cc.thread_id)
        print("-"*40)
        print( trace)
        print("-"*40)

    def test_watson_chain_agent(self):
        print("\n\n test_watson_chain_agent \n")
        mgr = get_agent_manager()
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("watson_llama_3_70_agent")
        if oae is None:
            raise ValueError("agent not found")
        owl_agent_runner =  mgr.build_agent_runner(oae.agent_id,"en")
        assert owl_agent_runner
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = owl_agent_runner.send_conversation(cc)
        assert rep.messages
        print(rep.messages[0].content)
        assert "don't know" in rep.messages[0].content

if __name__ == '__main__':
    unittest.main()
import unittest, sys, os
sys.path.append('./src')
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("../../.env")

from athena.routers.dto_models import ConversationControl
from athena.app_settings import get_config
from athena.llm.agent_anthropic import AnthropicClient

class TestBaseOwlAgent(unittest.TestCase):
    """
    Base Owl Agent has a basic prompt to interact with a LLM.
    Those test should help validating the main operations
    """
    
    
    def _test_start_conversation_with_claude(self):
        cfg = get_config()
        cfg.owl_agent_llm_model="claude-3-sonnet-20240229"
        cfg.owl_agent_llm_client_class="athena.llm.agent_anthropic.AnthropicClient"
        cc = ConversationControl()
        cc.prompt_ref = "default_prompt"
        cc.chat_history = []
        cc.type="chat" 
        agent = AnthropicClient()
        rep = agent.send_conversation(cc)
        assert rep


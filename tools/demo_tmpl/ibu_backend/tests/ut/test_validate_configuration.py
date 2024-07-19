"""
Read the assistant config for all assistant and try to instantiate all of them to validate each individual config
"""
import unittest
import os
import sys
from dotenv import load_dotenv
load_dotenv()

os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from athena.llm.assistants.assistant_mgr import get_assistant_manager

class TestValidateConfiguration(unittest.TestCase):
    
    def test_load_all_assistants(self):
        assistant_mgr = get_assistant_manager()
        for assistant_entity in assistant_mgr.get_assistants():
            print(f"Create instance for {assistant_entity}")
            assistant = assistant_mgr.build_assistant(assistant_entity,"en")
            assert assistant
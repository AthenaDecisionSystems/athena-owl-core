import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from athena.llm.prompts.prompt_mgr import get_prompt_manager

class TestPromptsManager(unittest.TestCase):
    """
    Prompts manager manages prompts and offer API to get a prompt for a locale.
    Unit tests at the component level.
    """


    def test_get_all_prompts(self):
        p_mgr=get_prompt_manager()
        l=p_mgr.get_prompts()
        assert l

    def test_get_default_prompt(self):
        # Should get the default prompt string
        p_mgr=get_prompt_manager()
        assert p_mgr
        p=p_mgr.get_prompt("default_prompt")
        assert p
        assert "questions based" in p

    def test_create_new_prompt(self):
        prompts = get_prompt_manager()
        prompts.add_prompt("a_test_prompt","en","You are a helpful assistant for an insurance company, if you do not the answer try to use the related tools")
        p=prompts.get_prompt("a_test_prompt","en")
        assert p
        assert "helpful assistant" in p

    def test_delete_prompt(self):
        p_mgr=get_prompt_manager()
        p_mgr.add_prompt("prompt-3","en","You are a helpful assistant")
   
        p_mgr.delete_prompt("prompt-3")
        p=p_mgr.get_prompt("prompt-3")
        assert "None" in p

    def test_update_prompt(self):
        p_mgr = get_prompt_manager()
        p_mgr.add_prompt("a_test_prompt_b","en","You are a helpful assistant for an insurance company, if you do not the answer try to use the related tools")
        p_mgr.update_prompt("a_test_prompt_b","en","You are not here")
        p2 =  p_mgr.get_prompt("a_test_prompt_b")
        assert p2
        assert "are not here" in p2
    
    def test_get_all_locale_of_a_prompt(self):
        locales = get_prompt_manager().get_prompt_locales("second_prompt")
        assert locales
        assert locales["en"]
        

if __name__ == '__main__':
    unittest.main()

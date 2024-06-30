import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from athena.llm.prompts.prompt_mgr import get_prompt_manager, OwlPromptEntity

class TestPromptsManager(unittest.TestCase):
    """
    Prompts manager manages prompts and offer API to get a prompt for a locale.
    Unit tests at the component level.
    """


    def test_get_all_prompts(self):
        p_mgr=get_prompt_manager()
        l=p_mgr.get_prompts()
        assert l
        assert l["default_prompt"]
        opeDict=l["default_prompt"]
        ope=OwlPromptEntity.model_validate(opeDict)
        assert ope.name == "default_prompt"
        print(ope.locales[0].text)

    def test_get_default_prompt(self):
        # Should get the default prompt string
        p_mgr=get_prompt_manager()
        assert p_mgr
        p=p_mgr.get_prompt("default_prompt")
        assert p
        assert "question based" in p

    def test_get_wrong_prompt(self):
        p_mgr=get_prompt_manager()
        assert p_mgr.get_prompt("unknown_prompt") == None
        
    def test_create_new_prompt(self):
        p_mgr = get_prompt_manager()
        p_mgr.add_prompt("a_test_prompt","en","You are a helpful assistant for an insurance company, if you do not the answer try to use the related tools")
        p=p_mgr.get_prompt("a_test_prompt","en")
        assert p
        assert "helpful assistant" in p

    def test_delete_prompt(self):
        p_mgr=get_prompt_manager()
        p_mgr.add_prompt("prompt-3","en","You are a helpful assistant")
   
        p_mgr.delete_prompt("prompt-3")
        p=p_mgr.get_prompt("prompt-3")
        assert p is None

    def test_update_prompt(self):
        p_mgr = get_prompt_manager()
        p_mgr.add_prompt("a_test_prompt_b","en","You are a helpful assistant for an insurance company, if you do not the answer try to use the related tools")
        p_mgr.update_prompt("a_test_prompt_b","en","You are not here")
        p2 =  p_mgr.get_prompt("a_test_prompt_b")
        assert p2
        assert "are not here" in p2
    
    def test_update_prompt_adding_a_locale(self):
        p_mgr = get_prompt_manager()
        p_mgr.add_prompt("a_test_prompt_b","en","You are a helpful assistant for an insurance company, if you do not the answer try to use the related tools")
        p_mgr.update_prompt("a_test_prompt_b","fr","Vous etes ici")
        p2 =  p_mgr.get_prompt("a_test_prompt_b", "fr")
        assert p2
        assert "Vous etes ici" in p2
        
    def test_get_all_locale_of_a_prompt(self):
        locales = get_prompt_manager().get_prompt_locales("second_prompt")
        assert locales
        assert locales["en"]
        
    def test_build_prompt_from_prompt_entity(self):
        print("\n\n --- test_build_prompt_instance_from_prompt_entity")
        p_mgr=get_prompt_manager()
        prompt = p_mgr.build_prompt("default_prompt","en")
        print(type(prompt))
        print(prompt)

if __name__ == '__main__':
    unittest.main()

"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from athena.glossary.glossary_mgr import CURRENT_LOCALE, DEFAULT_LOCALE
import json
from athena.app_settings import get_config
from functools import lru_cache
from pydantic import BaseModel, RootModel
from typing import List

"""
Prompt manager manages different prompts and support CRUD for prompt. In this
version the prompts is persisting on local file system.

The prompt persistence is a json with prompt_unique_key and the prompt string in different locale like:

{
 "default_prompt" : {
        "en": "Answer the user's...",
        "fr": "...."
 }
}

The path for persistence is defined in configuration as owl_prompts_path 

"""

_instance = None

class Prompts:
    """
    Use a cache for the Prompts in PROMPTS
    """
    def __init__(self):
        self.PROMPTS: dict

    def add_prompt(self, prompt_key: str, locale: str, prompt: str):
        """Adds a new prompt, using a key to the prompts inventory.

        Args:
            prompt_key (str): The key of the prompt.
            prompt (str): The prompt in the given locale.
            locale (str): The language of the translation. Defaults to "en".
        """
        entry = self.PROMPTS.get(prompt_key, None)
        if entry == None:
            entry = dict()
            self.PROMPTS[prompt_key] = entry
        entry[locale] = prompt


    def get_prompt(self, prompt_key: str, locale: str = CURRENT_LOCALE) -> str:
        entry = self.PROMPTS.get(prompt_key, None)
        if entry == None:
            return "None"
        else:
            res = entry.get(locale, entry.get(DEFAULT_LOCALE, None))
            if res == None:
                return "None"
            else:
                return res
    
    def get_prompt_locales(self, prompt_key: str) -> dict[str,str]:
        return self.PROMPTS.get(prompt_key, None)
    
    def delete_prompt(self, prompt_key: str) -> str:
        entry = self.PROMPTS.get(prompt_key, None)
        if entry != None:
            del self.PROMPTS[prompt_key]
            
    
    def get_prompts(self) -> dict[str,dict[str]]:
        return self.PROMPTS
    
    def save_prompts(self, path: str = "prompts.json"):
        """Save the entire prompts in external file."""
        with open(path, "w", encoding="utf-8") as of:
            json.dump(self.PROMPTS, of, indent=4, ensure_ascii=False)
        return path

    def update_prompt(self,prompt_key: str, locale: str, prompt: str):
        self.add_prompt(prompt_key,locale,prompt)
    
    def load_prompts(self, path: str = "prompts.json"):
        """Reads the prompts from a file."""
        with open(path, "r", encoding="utf-8") as f:
            self.PROMPTS = json.load(f)  # a dict with prompt key and locales
         

@lru_cache
def get_prompt_manager() -> Prompts:
    """ Factory to get access to unique instance of Prompts manager"""
    global _instance
    if _instance is None:
        path = get_config().owl_prompts_path
        if path is None:
            path="./athena/config/prompts.json"
        _instance = Prompts()
        _instance.load_prompts(path)
    return _instance


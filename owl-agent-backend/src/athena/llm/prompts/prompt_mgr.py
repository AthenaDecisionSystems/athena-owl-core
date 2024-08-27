"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from athena.glossary.glossary_mgr import CURRENT_LOCALE, DEFAULT_LOCALE
import json, yaml, uuid
from athena.app_settings import get_config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from functools import lru_cache
from pydantic import BaseModel, RootModel
from typing import List, Optional

"""
Prompt manager manages different prompts and support CRUD for prompt. In this
version the prompts is persisting on local file system.

The prompt persistence is a yaml with prompt_unique_key and the prompt string in different locale like:

{
 "default_prompt" : {
        "en": "Answer the user's...",
        "fr": "...."
 }
}

The path for persistence is defined in configuration as owl_prompts_path 

"""


class OwlPromptEntity(BaseModel):
    class localeStructure(BaseModel):
        locale: str
        text: str
    prompt_id: Optional[str] = str(uuid.uuid4())
    name: Optional[str]
    locales: list[localeStructure]

     
        
        
_instance = None

class Prompts:
    """
    Use a cache for the Prompts in PROMPTS
    """
    def __init__(self):
        self.PROMPTS: dict[OwlPromptEntity] = dict()

    def add_prompt(self, prompt_key: str, locale: str, text: str):
        """Adds a new prompt, using a key to the prompts inventory.

        Args:
            prompt_key (str): The key of the prompt.
            text (str): The prompt in the given locale.
            locale (str): The language of the translation. Defaults to "en".
        """
        entry = self.PROMPTS.get(prompt_key, None)
        if entry == None:
            localStruc= OwlPromptEntity.localeStructure(locale=locale, text=text)
            entry = OwlPromptEntity(name=prompt_key,locales=[localStruc])
            self.PROMPTS[prompt_key] = entry
        else:
            entry.locales.append(OwlPromptEntity.localeStructure(locale=locale, text=text))


    def get_prompt(self, prompt_key: str, locale: str = CURRENT_LOCALE) -> str | None:
        entry = self.PROMPTS.get(prompt_key, None)
        if entry == None:
            return None
        else:
            ope= OwlPromptEntity.model_validate(entry)
            for l in ope.locales:
                if l.locale == locale:
                    return l.text       
            return None
 

    def build_prompt(self, prompt_key: str, locale: str = CURRENT_LOCALE) -> BaseModel:
        if prompt_key is None or len(prompt_key) == 0:
            return None

        text = self.get_prompt(prompt_key, locale)
        if text == None:
            return None
        elif "context" in text:
            return ChatPromptTemplate.from_messages([
                    ("system", text),
                    MessagesPlaceholder(variable_name="chat_history", optional=True),
                    MessagesPlaceholder(variable_name="context", optional=True),
                    MessagesPlaceholder(variable_name="input", optional=True),
                    #("human", "{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
                ])
        else:
            return ChatPromptTemplate.from_messages([
                    ("system", text),
                    MessagesPlaceholder(variable_name="chat_history", optional=True),
                    MessagesPlaceholder(variable_name="input", optional=True),
                    #("human", "{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
                ])
        
    
    def get_prompt_locales(self, prompt_key: str) -> dict[str,str]:
        entry = self.PROMPTS.get(prompt_key, None)
        ope= OwlPromptEntity.model_validate(entry)
        a_dict = {}
        for ls in ope.locales:
            a_dict[ls.locale] = ls.text
        return a_dict
        
    def delete_prompt(self, prompt_key: str) -> str:
        entry = self.PROMPTS.get(prompt_key, None)
        if entry != None:
            del self.PROMPTS[prompt_key]
            
    
    def get_prompts(self) -> dict[OwlPromptEntity]:
        return self.PROMPTS
    
    def save_prompts(self, path: str = "prompts.yaml"):
        """Save the entire prompts in external file."""
        with open(path, "w", encoding="utf-8") as of:
            json.dump(self.PROMPTS, of, indent=4, ensure_ascii=False)
        return path

    def update_prompt(self,prompt_key: str, locale: str, text: str):
        entry = self.PROMPTS.get(prompt_key, None)
        if entry != None:
            ope= OwlPromptEntity.model_validate(entry)
            for l in ope.locales:
                if l.locale == locale:
                    l.text=text
                    return
            localStruc= OwlPromptEntity.localeStructure(locale=locale, text=text)
            ope.locales.append(localStruc)
             
        
    
    def load_prompts(self, path: str = "prompts.json"):
        """Reads the prompts from a file."""
        with open(path, "r", encoding="utf-8") as f:
            self.PROMPTS = yaml.load(f, Loader=yaml.FullLoader)  # a dict with prompts
         

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


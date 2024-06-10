"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import os, yaml, logging
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pydantic_yaml import parse_yaml_raw_as

class AppSettings(BaseSettings):
    model_config = ConfigDict(extra='allow')  # authorize adding attributes dynamically
    api_route: str = "/api/v1"
    version: str = "v0.0.1"
    owl_env_path: str = "../.env"
    logging_level: str = "INFO"
    logging_level_int: int = 0
    owl_env_path: str = "../.env"
    owl_agent_llm_client_class: str = "athena.llm.agent_openai.OpenAIClient"
    owl_agent_llm_model: str = "gpt-3.5-turbo-0125"
    owl_agent_decision_service_fct_name: str = "athena.itg.decisions.nba_ds_dummy.callDecisionService"
    owl_glossary_path: str = "./athena/config/glossary.json"
    owl_prompts_path: str = "./athena/config/prompts.json"
    owl_prompts_key_name: str = "default_prompt"

    owl_agent_content_collection_name: str = "base_collection"
    owl_agent_content_file_path: str = "./file_content"
    owl_agent_vs_path: str = "./chromadb"
    owl_agent_vs_url: str = ""
    owl_agent_vs_embedding_fct: str = ""


_config = None

# configuration is loaded only once and subsequent requests will use the cached configuration
@lru_cache
def get_config():
    global _config
    if _config is None:
        
        CONFIG_FILE= os.getenv("CONFIG_FILE")
        if CONFIG_FILE:
            print(f"reload config from file:{CONFIG_FILE}")
            with open(CONFIG_FILE, 'r') as file:
                _config = parse_yaml_raw_as(AppSettings,file.read())
        else:
            _config = AppSettings()
        if _config.logging_level == "INFO":
            _config.logging_level_int = logging.INFO
        if _config.logging_level == "DEBUG":
            _config.logging_level_int = logging.DEBUG
        else:
            _config.logging_level_int = logging.WARNING
    return _config

# mostly for testing
def set_config(config):
    global _config
    _config = config
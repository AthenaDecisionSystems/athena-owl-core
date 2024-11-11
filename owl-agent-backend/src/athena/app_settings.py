"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import os, yaml, logging
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pydantic_yaml import parse_yaml_raw_as
from importlib import import_module

class AppSettings(BaseSettings):
    model_config = ConfigDict(extra='allow')  # Allow adding attributes dynamically
    api_route: str = "/api/v1"
    app_index_path: str = "./athena/routers/index.html"
    version: str = "v0.0.1"
    owl_env_path: str = "../.env"
    logging_level: str = "INFO"
    logging_level_int: int = 0
    override_env: bool = True  # New setting to override the environment variables
    owl_agent_decision_service_fct_name: str = "athena.itg.decisions.nba_ds_dummy.callDecisionService"
    owl_glossary_path: str = "/app/athena/config/glossary.json"
    owl_prompts_path: str = "/app/athena/config/prompts.yaml"
    owl_prompts_key_name: str = "default_prompt"
    owl_agents_path: str = "/app/athena/config/agents.yaml"
    owl_tools_path: str = "/app/athena/config/tools.yaml"
    owl_agent_content_collection_name: str = "base_collection"
    owl_agent_content_file_path: str = "/app/file_content"
    owl_agent_vs_path: str = "/app/vs_db"
    owl_agent_vs_url: str = ""
    owl_agent_vs_class_name: str = "langchain_milvus.Milvus"
    owl_agent_vs_embedding_fct: str = "OpenAIEmbeddings"
    owl_agent_vs_embedding_fct_model: str = "text-embedding-3-large"
    owl_agent_llm_client_class: str = ""
    owl_agent_llm_history_length: int = 5
    owl_agent_llm_model: str = ""
    owl_agent_default_agent: str = "openai_chain_agent"
    owl_agent_tool_factory_class: str = "athena.llm.tools.tool_mgr.DefaultToolInstanceFactory"
    # Add OWL_CLIENTS for CORS origins
    owl_clients: str = "http://localhost:3000"  # Comma-separated origins

    def get_tool_factory(self):
        module_path, class_name = self.owl_agent_tool_factory_class.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        return klass()


_config = None

# Configuration is loaded only once and subsequent requests will use the cached configuration
@lru_cache
def get_config():
    global _config
    if _config is None:
        CONFIG_FILE = os.getenv("CONFIG_FILE")
        if CONFIG_FILE:
            print(f"Reload config from file: {CONFIG_FILE}")
            with open(CONFIG_FILE, 'r') as file:
                _config = parse_yaml_raw_as(AppSettings, file.read())
        else:
            _config = AppSettings()

        # Set logging_level_int based on logging_level
        if _config.logging_level.upper() == "INFO":
            _config.logging_level_int = logging.INFO
        elif _config.logging_level.upper() == "DEBUG":
            _config.logging_level_int = logging.DEBUG
        else:
            _config.logging_level_int = logging.WARNING
    return _config

# Mostly for testing
def set_config(config):
    global _config
    _config = config

def config_reload():
    global _config
    _config = None
    get_config()
    return "Reload configuration done"

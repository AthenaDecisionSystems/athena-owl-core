"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_ibm import WatsonxLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from ..routers.dto_models import ConversationControl
from .base_owl_agent import BaseOwlAgent
from ..app_settings import get_config

class WatsonXClient(BaseOwlAgent):

    def assess_what_prompt_to_use(self,conversationControl:ConversationControl):
        if conversationControl.type == "chat":
            prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
            ])
        else:
            prompt = ChatPromptTemplate.from_messages([
                        ("system", 
                        """
                        You always answer the questions with markdown formatting. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.
                        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. 
                        Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

                        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don'\''t know the answer to a question, please don'\''t share false information.
                        """),
                    ("user", "{input}")
                ])
        return prompt

    def get_model(self, stream, callbacks):
        self.parameters = {
            "decoding_method": "sample",
            "max_new_tokens": 100,
            "min_new_tokens": 1,
            "temperature": 0.2,
            "top_k": 50,
            "top_p": 1,
        }
        config = get_config()
        return WatsonxLLM(
            model_id=config["watsonx_ai_model"],
            url=config["watsonx_ai_url"],
            project_id=config["watsonx_ai_project_id"],
            params=self.parameters
        )
    
    def get_agent(self, model, prompt, tools ):
        # TO DO
        return None
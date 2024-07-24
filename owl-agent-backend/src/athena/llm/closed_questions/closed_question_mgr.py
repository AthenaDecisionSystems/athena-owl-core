"""
Copyright 2024 Athena Decision Systems
@author Jean-Christophe Jardinier

"""

from pydantic import BaseModel
import uuid

# THIS IS THE USE CASE IN WHICH CLOSED QUESTIONS ARE USED:
# 1. given the goal at hand, define the agent state to keep named business entities needed by the decision service
# 2. initialize the named entities as empty or by fetching them by ID from a datasource
# 3. call the decision service iteratively until we reach a conclusion
#   - use closed questions to enrich the business entities stored in the AgentState and needed by the Decision Service

# TODO: instead of representing the data_type attributes, we should have a representation of the different types.

# a closed question entity can be read from a yaml configuration file or generated dynamically by an "interactive" decision service
class OwlClosedQuestionEntity(BaseModel):
    """
    Entity definition for closed questions
    Closed questions are used to enrich the objects kept as named parameters in the LangGraph AgentState
    """
    class localeStructure(BaseModel):
        locale: str
        text: str

    question_id: str = str(uuid.uuid4())
    key_name: str = ""
    data_type: str = ""
    locales: list[localeStructure]

"""
# this is a sample yaml describing a closed question

age_of_the_captain:
  - question_id: age_oF_the_captain
  - key_name: "the boat.captain.age"      # used to look for a question
  - labels:
    - locale: en
      text: |
        "What is the age of the captain?"
    - locale: fr
      text: |
        "Quel est l'age du capitaine ?"
  - data_type: integer
"""


class OwlDecisionSignatureEntity(BaseModel):
    class namedParameter(BaseModel):
        name: str
        alias: str
        data_type: str

"""
# this is a sample yaml defining an OwlDecisionSignatureEntity
# call to decision service = tool with parameters

parameters:
  - name: "boat"              # id using in AgentState dictionary
    alias: "the boat"         # optional, this can be the param name used in decision service
    data_type: "org.myrace.Boat"
  - name: "race"
    alias: "the race"
    data_type: "org.myrace.Race"
  - name: "harbor"
    alias: "the harbor"
    data_type: "org.myrace.Harbor"
"""

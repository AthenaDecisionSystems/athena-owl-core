"""
Copyright 2024 Athena Decision Systems
@author Jean-Christophe Jardinier

"""

from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
import uuid

# THIS IS THE USE CASE IN WHICH CLOSED QUESTIONS ARE USED:
# 1. given the goal/intent at hand, define the agent state to keep named business entities needed by the decision service
# 2. initialize the named entities as empty or by fetching them by ID from a datasource
# 3. call the decision service iteratively until we reach a conclusion
#   - use closed questions to enrich the business entities stored in the AgentState and needed by the Decision Service


class DataTypeEnum(str, Enum):
    boolean_type = 'Boolean'
    text_type = 'Text'
    integer_type = 'Integer'
    double_type = 'Number'          # a double float
    #big_integer_type = 'BigInteger'
    #big_decimal_type = 'BigDecimal'
    date_type = 'Date'              # The most common ISO Date Format yyyy-MM-dd — for example, "2000-10-31".
    datetime_type = 'DateTime'      # The most common ISO Date Time Format yyyy-MM-dd'T'HH:mm:ss.SSSXXX — for example, "2000-10-31T01:30:00.000-05:00".

class LabelValuePair(BaseModel):
    label: str                      # label shown in the UI in a dropdown list
    value: str

class EnumRestrictions(BaseModel):
    possible_values: Optional[List[LabelValuePair]] = None

class TextRestrictions(BaseModel):
    regex: Optional[str] = None       # only applicable if data_type is text
    minLength: Optional[int] = None   # minimum string length
    maxLength: Optional[int] = None   # maximum string length

class RangeRestrictions(BaseModel):
    min: Optional[str] = None         # min string will be converted to integer, floating point number, date or datetime depending on the data_type
    max: Optional[str] = None         # max string will be converted to integer, floating point number, date or datetime depending on the data_type
    step: Optional[str] = None

class DataRestrictions(BaseModel):    # this object will populate one of the three following members
    range: Optional[RangeRestrictions] = None
    text: Optional[TextRestrictions] = None
    enumeration: Optional[EnumRestrictions] = None
"""
    possible_values: Optional[List[LabelValuePair]] = None
    regex: Optional[str] = None       # only applicable if data_type is text
    min: Optional[str] = None         # min string will be converted to integer, floating point number, date or datetime depending on the data_type
    max: Optional[str] = None         # max string will be converted to integer, floating point number, date or datetime depending on the data_type
    minLength: Optional[int] = None   # minimum string length
    maxLength: Optional[int] = None   # maximum string length
"""

class LocalizedText(BaseModel):
  locale: str
  text: str

# a closed question entity can be read from a yaml configuration file or generated dynamically by an "interactive" decision service
class OwlClosedQuestionEntity(BaseModel):
    """
    Entity definition for closed questions
    Closed questions are used to enrich the objects kept as named parameters in the LangGraph AgentState
    """

    question_id: str = str(uuid.uuid4())
    key_name: str
    labels: list[LocalizedText]

    data_type: DataTypeEnum
    restrictions: Optional[DataRestrictions] = None   # e.g. number in [0.0, 100.0] => restrictions.min = "0.0", restrictions.max = "100.0"
    default_value: Optional[str] = None               # can be used to propose a default value in the UI

"""
# this is a sample yaml describing a closed question

power_of_the_vehicle_engine:
  - question_id: power_of_the_vehicle_engine
  - key_name: "the vehicle.engine.power"      # used to look for a question and reinject a value in the agent state
  - labels: 
    - locale: en
      text: "What is the power of the vehicle's engine?"
    - locale: fr
      text: "Quelle est la puissance du moteur du véhicle?"
  - data_type: "Number"
  - restrictions:
    - range:
      - min: "0.0"
  - default_value: "100.0"
"""



class OwlDecisionSignatureEntity(BaseModel):

    class namedParameter(BaseModel):
        name: str
        alias: Optional[str] = None       # if provided, the alias is used to find a named parameter in the list of decision service inputs
        data_type: str

    parameters: list[namedParameter]

"""
# this is a sample yaml defining an OwlDecisionSignatureEntity
# call to decision service = tool with parameters

parameters:
  - name: "vehicle"              # id using in AgentState dictionary, it has to be a valid Python variable name. In particular, it cannot contain spaces
    alias: "the vehicle"         # optional, this can be the param name used in decision service
    data_type: "org.dt.cartax.Vehicle"
  - name: "requester"
    alias: "the requester"
    data_type: "org.dt.cartax.Requester"
  - name: "declaration"
    alias: "the declaration"
    data_type: "org.dt.cartax.Declaration"
"""

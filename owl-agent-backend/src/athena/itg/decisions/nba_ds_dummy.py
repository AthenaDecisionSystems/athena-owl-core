import json

def callDecisionService(client_id : int, intentionToLeave: bool, locale: str):
    rep_str="""
{"__DecisionID__":"de8308ab-b880-42af-9fd3-3e4d719f74f80",
 "response": {
    "actions": [
        {"typeDisc__":"ResendTo",
         "recipient":"ClaimsExpert",
         "suggestion":null}],
         "missingInfoElements":[],
         "outputTraces":
         ["high score"],
         "explanationCode":null}}
"""
    return json.loads(rep_str)


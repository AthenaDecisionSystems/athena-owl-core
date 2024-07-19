"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

import requests, logging, json

#from athena.glossary.glossary_mgr import build_get_glossary, Glossary

from ibu.itg.ds.loanapp_borrower_repo_mock import BorrowerRepositoryInMem
from ibu.app_settings import get_config


LOGGER = logging.getLogger(__name__)

DS_URL: str = get_config().app_loanapp_decision_service_url # type: ignore

def callRuleExecutionServer(payload: str):
    response = requests.post(
        DS_URL, 
        payload,
        headers={"Content-Type": "application/json"}
    )
    return response



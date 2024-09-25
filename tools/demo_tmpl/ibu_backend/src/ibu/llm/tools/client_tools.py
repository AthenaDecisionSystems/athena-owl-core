import logging, uuid, datetime
from ibu.app_settings import get_config
from importlib import import_module
from typing import  Any

from ibu.itg.ds.loanapp_borrower_repo_mock import LoanApplicationClientRepositoryInterface
from ibu.itg.ds.pydantic_generated_model import Loan, Request
from ibu.itg.decisions.next_best_action_ds_client import callRuleExecutionServer
from athena.llm.tools.tool_mgr import DefaultToolInstanceFactory
from langchain_community.tools.tavily_search import TavilySearchResults

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger(__name__)


_loan_client: LoanApplicationClientRepositoryInterface = None

def build_or_get_loan_client_repo() -> LoanApplicationClientRepositoryInterface:
    global _loan_client
    if not _loan_client:
        config = get_config()
        module_path, class_name = config.app_borrower_repository.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        LOGGER.debug(f"---> klass {klass}")
        _loan_client= klass()
        LOGGER.debug("Created repository for client")
    return _loan_client



def get_client_by_name(first_name: str, last_name: str) -> str | None:
    """get borrower client information given his or her name"""
    return build_or_get_loan_client_repo().get_client_by_name_json(first_name,last_name)

def define_next_best_action_with_decision(loanRequest: Loan, first_name: str, last_name: str ):
    """perform the loan application request assessment for the given borrower name
    """
    if loanRequest and type(loanRequest) == Loan:
        borrower =  build_or_get_loan_client_repo().get_client_by_name(first_name=first_name, last_name=last_name)
        ds_request = Request(__DecisionID__= str(uuid.uuid4),borrower=borrower, loan=loanRequest)
        payload: str = ds_request.model_dump_json()
        return callRuleExecutionServer(payload)
    else:
        return None

def assess_loan_app_with_decision(loan_amount: int, duration: int,   first_name: str, last_name: str, yearlyRepayment: int):
    loanRequest= Loan(duration=duration, 
                      yearlyRepayment=yearlyRepayment,
                      yearlyInterestRate=4,
                      amount=loan_amount)
    
    borrower =  build_or_get_loan_client_repo().get_client_by_name(first_name=first_name, last_name=last_name)
    ds_request = Request(borrower=borrower, loan=loanRequest) # type: ignore
    payload: str = ds_request.model_dump_json()
    LOGGER.info(f"@@@> decision service request {payload}")
    rep = callRuleExecutionServer(payload)
    LOGGER.info(f"@@@> decision service response {rep.text}")
    return rep.text

    



    
class IbuLoanToolInstanceFactory(DefaultToolInstanceFactory):
    methods = { "get_client_by_name": get_client_by_name, 
           "assess_loan_app_with_decision": assess_loan_app_with_decision}
    arg_schemas = { "Loan": Loan}
    
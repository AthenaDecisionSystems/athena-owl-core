"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
from typing import List
import json
from ibu.itg.ds.pydantic_generated_model import Borrower

class LoanApplicationClientRepositoryInterface:

    def get_client_by_name(self,first_name: str, last_name: str) -> Borrower | None:
        return None
    
    
    def get_client_by_name_json(self,first_name: str, last_name: str) -> str | None:
        return None
    
    def get_all_clients_json(self) -> str | None:
        return None
    
    def get_all_clients(self) -> list[Borrower] | None:
        return None
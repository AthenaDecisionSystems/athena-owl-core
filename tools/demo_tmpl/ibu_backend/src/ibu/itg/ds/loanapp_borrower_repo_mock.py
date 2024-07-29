"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
from ibu.itg.ds.loanapp_borrower_repo import LoanApplicationClientRepositoryInterface
from ibu.itg.ds.pydantic_generated_model import Borrower

class BorrowerRepositoryInMem(LoanApplicationClientRepositoryInterface):

    def __init__(self):
        self.BORROWERDB = dict()
        self.initialize_client_db()

    def add_client(self, client: Borrower):
        self.BORROWERDB[client.name] = client

    def get_client(self, id: int) -> Borrower:
        logging.info(f"---> In client mock get with id: {id}")
        return self.BORROWERDB.get(id, None)

    def initialize_client_db(self):
        self.add_client(Borrower(name = "robert dupont",
                            yearlyIncome = 50000,
                            creditScore = 180
                            ))
        self.add_client(Borrower(name = "joe hurt",
                            yearlyIncome = 30000,
                            creditScore = 700,
                            ))
        self.add_client(Borrower(name = "marie durand",
                            yearlyIncome = 80000,
                            creditScore = 500
                            ))
        self.add_client(Borrower(name = "jean martin",
                          
                            yearlyIncome = 100000,
                          
                            creditScore = 500,
                           
                            ))
        self.add_client(Borrower(name = "sophie lefevre",
                          
                            yearlyIncome = 40000,
                           
                            creditScore = 500,
                           
                            ))
        self.add_client(Borrower(name = "pierre moreau",
                            yearlyIncome = 120000,
                            creditScore = 500
                            ))
        rsmith = Borrower(name = "robert smith",
                            yearlyIncome = 140000,
                            creditScore = 150,
                            )
        self.add_client(rsmith)


    def get_client_by_name(self, first_name: str, last_name: str) -> Borrower | None:
        for client in self.BORROWERDB.values():
            if client.name == first_name.lower() + " " + client.lastName.lower():
                return client
        return None


    def get_client_by_name_json(self, first_name: str, last_name: str) -> str:
        client = self.get_client_by_name(first_name, last_name)
        if client:
            return client.model_dump_json()
        return f"No client found with name '{first_name} - {last_name}'"

    
    def get_all_clients_json(self) -> str:
        return json.dumps([client.model_dump() for client in self.BORROWERDB.values()], indent=4)


    def get_all_clients(self) -> list[Borrower]:
        return list(self.BORROWERDB.values())










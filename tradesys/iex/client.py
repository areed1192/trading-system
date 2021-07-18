import requests


class InvestorExchangeClient():

    def __init__(self, api_key: str) -> None:

        self._api_key = api_key
    
    
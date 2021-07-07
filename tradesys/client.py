
from typing import List
from typing import Dict
from typing import Union
from tradesys.keyvault.client import TradingFactoryKeyVault
from tradesys.utils.templates import AzureTemplates
from tradesys.utils.credentials import TradingCredentials

class TradingSystem():

    def __init__(self):
        
        self.templates_client = AzureTemplates()
        self.credentials_client = TradingCredentials()

    def __repr__(self):
        pass

    def key_vault(self) -> TradingFactoryKeyVault:

        return TradingFactoryKeyVault(trading_sys_client=self)

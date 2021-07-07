from tradesys.utils.templates import AzureTemplates
from tradesys.utils.credentials import TradingCredentials
from tradesys.mgmt.storage import TradingFactoryStorage
from tradesys.mgmt.key_vault import TradingFactoryKeyVault

class TradingSystem():

    def __init__(self):

        self.templates_client = AzureTemplates()
        self.credentials_client = TradingCredentials()

    def __repr__(self):
        return "<TradingSystem Initialized=True, Active=True>"

    @property
    def key_vault_client(self) -> TradingFactoryKeyVault:
        return TradingFactoryKeyVault(trading_sys_client=self)

    @property
    def storage_client(self) -> TradingFactoryStorage:
        return TradingFactoryStorage(trading_sys_client=self)
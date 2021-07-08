from tradesys.utils.templates import AzureTemplates
from tradesys.utils.credentials import TradingCredentials
from tradesys.mgmt.storage import TradingFactoryStorageClient
from tradesys.mgmt.key_vault import TradingFactoryVaultClient
from tradesys.mgmt.sql import TradingFactorySqlClient


class TradingSystem():

    def __init__(self):

        self.templates_client = AzureTemplates()
        self.credentials_client = TradingCredentials()

    def __repr__(self):
        return "<TradingSystem Initialized=True, Active=True>"

    @property
    def vault_mgmt_client(self) -> TradingFactoryVaultClient:
        """Returns the Key Vault Management client for the Trading Factory.
        Can be used to manage different Azure Key Vault Services.

        ### Returns:
        ----
        TradingFactoryVaultClient:
            An authenticated instance of a `KeyVaultManagementClient`.
        """

        return TradingFactoryVaultClient(trading_sys_client=self)

    @property
    def storage_mgmt_client(self) -> TradingFactoryStorageClient:
        """Returns the Storage Management client for the Trading Factory.
        Can be used to manage different Azure Storage Services.

        ### Returns:
        ----
        TradingFactoryStorageClient:
            An authenticated instance of a `StorageManagementClient`.
        """

        return TradingFactoryStorageClient(trading_sys_client=self)

    @property
    def sql_mgmt_client(self) -> TradingFactorySqlClient:
        """Returns the SQL Management client for the Trading Factory.
        Can be used to manage different Azure SQL Services.

        ### Returns:
        ----
        TradingFactorySqlClient:
            An authenticated instance of a `TradingFactorySqlClient`.
        """

        return TradingFactorySqlClient(trading_sys_client=self)

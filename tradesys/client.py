from tradesys.utils.templates import AzureTemplates
from tradesys.utils.credentials import TradingCredentials
from tradesys.mgmt.storage import TradingFactoryStorageClient
from tradesys.mgmt.key_vault import TradingFactoryVaultClient
from tradesys.mgmt.sql import TradingFactorySqlClient
from tradesys.mgmt.data_factory import TradingFactoryManagementClient


class TradingSystem():

    def __init__(self):
        """Initializes the `TradingSystem` object."""

        self.templates_client = AzureTemplates()
        self.credentials_client = TradingCredentials()

    def __repr__(self):
        return "<TradingSystem Initialized=True, Active=True>"

    @property
    def vault_mgmt_client(self) -> TradingFactoryVaultClient:
        """Returns the Azure Key Vault Management Client.

        ### Overview:
        ----
        This can be  used to manage a azure key vault resources directly from
        the Trading System client. Operations, include creating, deleting,
        and listing. Additionally, you can access the manager directly to
        perform more detailed operations.

        ### Returns:
        ----
        TradingFactoryVaultClient:
            An authenticated instance of a `KeyVaultManagementClient`.
        """

        return TradingFactoryVaultClient(trading_sys_client=self)

    @property
    def storage_mgmt_client(self) -> TradingFactoryStorageClient:
        """Returns the Azure Storage Management Client.

        ### Overview:
        ----
        This can be  used to manage a azure storage resources directly from
        the Trading System client. Operations, include creating, deleting,
        and listing. Additionally, you can access the manager directly to
        perform more detailed operations.

        ### Returns:
        ----
        TradingFactoryStorageClient:
            An authenticated instance of a `StorageManagementClient`.
        """

        return TradingFactoryStorageClient(trading_sys_client=self)

    @property
    def sql_mgmt_client(self) -> TradingFactorySqlClient:
        """Returns the Azure SQL Management Client.

        ### Overview:
        ----
        This can be  used to manage a azure sql resource directly from
        the Trading System client. Operations, include creating, deleting,
        and listing. Additionally, you can access the manager directly to
        perform more detailed operations.

        ### Returns:
        ----
        TradingFactorySqlClient:
            An authenticated instance of a `TradingFactorySqlClient`.
        """

        return TradingFactorySqlClient(trading_sys_client=self)

    @property
    def factory_mgmt_client(self) -> TradingFactoryManagementClient:
        """Returns the Azure Data Factory Management Client.

        ### Overview:
        ----
        This can be  used to manage a data factory resource directly from
        the Trading System client. Operations, include creating, deleting,
        and listing. Additionally, you can access the manager directly to
        perform more detailed operations.

        ### Returns:
        ----
        TradingFactoryManagementClient:
            An authenticated instance of a `TradingFactoryManagementClient`.
        """

        return TradingFactoryManagementClient(trading_sys_client=self)

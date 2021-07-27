from tradesys.utils.templates import AzureTemplates
from tradesys.utils.credentials import TradingCredentials

from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient


class TradingSystem():

    def __init__(self):
        """Initializes the `TradingSystem` object."""

        self.templates_client = AzureTemplates()
        self.credentials_client = TradingCredentials()

    def __repr__(self):
        return "<TradingSystem Initialized=True, Active=True>"

    @property
    def vault_mgmt_client(self) -> KeyVaultManagementClient:
        """Returns the Azure Key Vault Management Client.

        ### Overview:
        ----
        This can be  used to manage a azure key vault resources directly from
        the Trading System client. Operations, include creating, deleting,
        and listing. Additionally, you can access the manager directly to
        perform more detailed operations.

        ### Returns:
        ----
        KeyVaultManagementClient:
            An authenticated instance of a `KeyVaultManagementClient`.
        """

        # Define a new `KeyVaultManagementClient`.
        key_vault_mgmt_client = KeyVaultManagementClient(
            credential=self.credentials_client.azure_credentials,
            subscription_id=self.credentials_client.subscription_id
        )

        return key_vault_mgmt_client

    @property
    def storage_mgmt_client(self) -> StorageManagementClient:
        """Returns the Azure Storage Management Client.

        ### Overview:
        ----
        This can be  used to manage a azure storage resources directly from
        the Trading System client. Operations, include creating, deleting,
        and listing. Additionally, you can access the manager directly to
        perform more detailed operations.

        ### Returns:
        ----
        StorageManagementClient:
            An authenticated instance of a `StorageManagementClient`.
        """

        # Create a new `StorageManagementClient`.
        storage_mgmt_client = StorageManagementClient(
            credential=self.credentials_client.azure_credentials,
            subscription_id=self.credentials_client.subscription_id
        )

        return storage_mgmt_client

    @property
    def sql_mgmt_client(self) -> SqlManagementClient:
        """Returns the Azure SQL Management Client.

        ### Overview:
        ----
        This can be  used to manage a azure sql resource directly from
        the Trading System client. Operations, include creating, deleting,
        and listing. Additionally, you can access the manager directly to
        perform more detailed operations.

        ### Returns:
        ----
        SqlManagementClient:
            An authenticated instance of a `TradingFactorySqlClient`.
        """

        # Create a new `SqlManagmentClient`.
        sql_mgmt_client = SqlManagementClient(
            credentials=self.credentials_client.azure_credentials,
            subscription_id=self.credentials_client.subscription_id
        )

        return sql_mgmt_client

    @property
    def factory_mgmt_client(self) -> DataFactoryManagementClient:
        """Returns the Azure Data Factory Management Client.

        ### Overview:
        ----
        This can be  used to manage a data factory resource directly from
        the Trading System client. Operations, include creating, deleting,
        and listing. Additionally, you can access the manager directly to
        perform more detailed operations.

        ### Returns:
        ----
        DataFactoryManagementClient:
            An authenticated instance of a `TradingFactoryManagementClient`.
        """

        # Create a new `DataFactoryManagmentClient`.
        data_factory_mgmt_client = DataFactoryManagementClient(
            credential=self.credentials_client.azure_credentials,
            subscription_id=self.credentials_client.subscription_id
        )

        return data_factory_mgmt_client

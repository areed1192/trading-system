import unittest

from unittest import TestCase
from tradesys.client import TradingSystem
from tradesys.utils.templates import AzureTemplates
from tradesys.utils.credentials import TradingCredentials

from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient


class TradingFactorySessionTest(TestCase):

    """Will perform a unit test for the `TradingSystem`."""

    def setUp(self) -> None:
        """Set up the `TradingSystem` Client."""

        # Initialize our Trading System.
        self.trading_system_client = TradingSystem()

    def test_creates_instance_of_trading_system_client(self):
        """Create an instance and make sure it's a `TradingSystem` object."""

        self.assertIsInstance(
            self.trading_system_client,
            TradingSystem
        )

    def test_creates_instance_of_trading_system_credentials(self):
        """Create an instance and make sure it's a `TradingCredentials` object."""

        self.assertIsInstance(
            self.trading_system_client.credentials_client,
            TradingCredentials
        )

    def test_creates_instance_of_trading_system_sql_mgmt(self):
        """Create an instance and make sure it's a `SqlManagementClient` object."""

        self.assertIsInstance(
            self.trading_system_client.sql_mgmt_client,
            SqlManagementClient
        )

    def test_creates_instance_of_trading_system_factory_mgmt(self):
        """Create an instance and make sure it's a `DataFactoryManagementClient` object."""

        self.assertIsInstance(
            self.trading_system_client.factory_mgmt_client,
            DataFactoryManagementClient
        )

    def test_creates_instance_of_trading_system_storage_mgmt(self):
        """Create an instance and make sure it's a `StorageManagementClient` object."""

        self.assertIsInstance(
            self.trading_system_client.storage_mgmt_client,
            StorageManagementClient
        )

    def test_creates_instance_of_trading_system_vault_mgmt(self):
        """Create an instance and make sure it's a `KeyVaultManagementClient` object."""

        self.assertIsInstance(
            self.trading_system_client.vault_mgmt_client,
            KeyVaultManagementClient
        )

    def test_creates_instance_of_trading_system_templates(self):
        """Create an instance and make sure it's a `AzureTemplates` object."""

        self.assertIsInstance(
            self.trading_system_client.templates_client,
            AzureTemplates
        )

    def tearDown(self) -> None:
        """Teardown the `TradingSystem` Client."""

        del self.trading_system_client


if __name__ == '__main__':
    unittest.main()

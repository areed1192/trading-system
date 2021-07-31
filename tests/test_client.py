import unittest

from unittest import TestCase
from configparser import ConfigParser

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
        """Set up the `TradingSystem` Client Object."""

        # Initialize the Parser.
        config = ConfigParser()

        # Read the file.
        config.read('configs/config.ini')

        # Get the specified credentials.
        config.get('main', '')

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a <PLACEHOLDER>."""
        pass

    def tearDown(self) -> None:
        """Teardown the <PLACEHOLDER> Client."""
        pass


if __name__ == '__main__':
    unittest.main()

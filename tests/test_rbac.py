import pathlib
import unittest
from unittest import TestCase
from configparser import ConfigParser
from tradesys.rbac.client import RoleBasedAccessControl


class RoleBasedAccessControlSessionTest(TestCase):

    """Will perform a unit test for the `RoleBasedAccessControl` object."""

    def setUp(self) -> None:
        """Set up the `RoleBasedAccessControl` object."""

        # Initialize the Parser.
        config = ConfigParser()
        config.read('config/config.ini')
        self.subscription_id = config.get(
            'rbac_credentials', 'subscription_id')
        self.subscription_name = config.get(
            'rbac_credentials', 'subscription_name')

        # Initialize the Client.
        self.rbac_client = RoleBasedAccessControl(
            subscription_id=self.subscription_id
        )

    def test_creates_instance_of_rbac_client(self):
        """Create an instance and make sure it's a `RoleBasedAccessControl` object."""

        self.assertIsInstance(
            self.rbac_client,
            RoleBasedAccessControl
        )

    def test_check_azure_cli(self):
        """Tests the `check_for_azure_cli` method`."""

        self.assertTrue(self.rbac_client.check_for_azure_cli())

    def test_check_set_subscription_acct(self):
        """Tests the `set_subscription_account` method`."""

        check_msg_explicit = {"message": f"Azure Subscription set to {self.subscription_name}."}
        check_msg_default = {"message": f"Azure Subscription set to {self.subscription_id}."}

        # Set it explicitly.
        msg_explicit = self.rbac_client.set_subscription_account(
            subscription=self.subscription_name
        )

        # Set it using default value.
        msg_default = self.rbac_client.set_subscription_account()

        self.assertDictEqual(msg_explicit, check_msg_explicit)
        self.assertDictEqual(msg_default, check_msg_default)

    def test_check_create_rbac(self):
        """Tests the `create_rbac` method`."""

        # First let's create it.
        rbac_credentials = self.rbac_client.create_rbac(
            rbac_name='UnitTestRbacClient'
        )

        # Make sure the results has a client ID.
        self.assertIn('clientId', rbac_credentials)

        # Double check using the Azure CLI.
        self.rbac_client.az_cli.invoke(
            args=['ad', 'app', 'list', '--display-name', 'UnitTestRbacClient']
        )

        # Grab the result.
        result = self.rbac_client.az_cli.result.result
        self.assertIsNotNone(result)

        # Delete the App.
        self.rbac_client.az_cli.invoke(
            args=['ad', 'app', 'delete', '--id', result[0]['appId']]
        )

    def test_create_config_file(self):
        """Tests the `generate_config_files` method`."""

        self.rbac_client.generate_config_files(file_name='config/my_new_config.ini')
        new_config_location = pathlib.Path('config/my_new_config.ini')
        self.assertTrue(new_config_location.exists())

    def test_create_command_file(self):
        """Tests the `generate_config_files` method`."""

        self.rbac_client.generate_batch_script(file_name='config/my_new_config.cmd')
        new_config_location = pathlib.Path('config/my_new_config.cmd')
        self.assertTrue(new_config_location.exists())

    def tearDown(self) -> None:
        """Teardown the `RoleBasedAccessControl` Client."""

        del self.rbac_client


if __name__ == '__main__':
    unittest.main()

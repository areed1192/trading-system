import json
import pathlib
import subprocess
import textwrap
from configparser import ConfigParser
from azure.cli.core import get_default_cli


class RoleBasedAccessControl():

    def __init__(self, subscription_id: str) -> None:
        """Initializes the `RoleBasedAccessControl` object that will be used to
        create a new RBAC role for the trading system.

        ### Parameters
        ----
        subscription_id : str
            Your Azure Subscription ID.
        """

        self.dump_file = open('config/azure_cli.txt', 'w+')
        self.az_cli = get_default_cli()

    def check_for_azure_cli(self) -> bool:
        """Checks whether we can run Azure commands.

        ### Returns
        ----
        bool:
            `True` if the command ran succesfully, and `False`
            otherwise.
        """

        self.az_cli.invoke(
            args=['account', 'show'],
            initial_invocation_data=None,
            out_file=self.dump_file
        )

        if self.az_cli.result.result:
            return True
        elif self.az_cli.result.error:
            return False

    def set_subscription_account(self, subscription_name: str) -> dict:
        """Sets the subscription that we wanth the RBAC to be created for.

        ### Parameters
        ----
        subscription_name (str):
            Your Azure subscription name.

        ### Returns
        ----
        dict:
            A message specifying whether the operation was successful
            or not.
        """

        self.az_cli.invoke(
            args=['account', 'set', '--subscription', subscription_name],
            initial_invocation_data=None,
            # out_file=self.dump_file
        )

        if self.az_cli.result.result == None:
            return {"message": f"Azure Subscription set to {subscription_name}."}
        elif self.az_cli.result.error:
            return {"message": "Azure operation failed."}

    def create_rbac(self, subscription_name: str, rbac_name: str) -> dict:
        """Creats a new role based service principal using the Azure CLI.

        ### Parameters
        ----
        subscription_name (str):
            Your Azure subscription name.

        rbac_name (str):
            The name you want your RBAC object to be.

        ### Returns
        ----
        dict:
            A `RBAC` resource.
        """

        # Step 1: Set the `AzureSubscription` account.
        self.set_subscription_account(
            subscription_name=subscription_name
        )

        config_folder = pathlib.Path(__file__).parents[2].joinpath('config/')

        # Step 2: Ensure Config folder.
        if not config_folder.exists():
            config_folder.mkdir()

        # Step 3: Define the Azure Command.
        azcmd = "az ad sp create-for-rbac --name " + rbac_name + \
            " --skip-assignment --sdk-auth > config/azure_rbac_auth_sp.json"

        # Run it.
        try:
            subprocess.run(azcmd, shell=True).returncode
        except:
            raise subprocess.SubprocessError("RBAC Couldn't be created.")

        # Read the credentials.
        with config_folder.joinpath('azure_rbac_auth_sp.json').open(mode='r') as rbac_file:
            rbac_credentials = json.load(fp=rbac_file)

        return rbac_credentials
    
    def generate_config_files(self) -> None:

        # Load the RBAC Config.
        with open(file="config/azure_rbac_auth_sp.json", mode='r') as rbac_file:
            rbac_config = json.load(fp=rbac_file)

        # Initialize the Parser.
        config = ConfigParser()

        # Add the Section.
        config.add_section('rbac_credentials')
        config.add_section('azure_subscriptions')

        # Set the Values.
        config.set('rbac_credentials', 'client_id', rbac_config['clientId'])
        config.set('rbac_credentials', 'tenant_id', rbac_config['tenantId'])
        config.set('rbac_credentials', 'client_secret', rbac_config['clientSecret'])

        # Write the file.
        with open(file='config/config.ini', mode='w+') as f:
            config.write(fp=f)

    def set_environment_variables(self) -> dict:
        pass

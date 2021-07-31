import json
import pathlib
import subprocess
import textwrap
from typing import Union
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

        self.subscription_id = subscription_id
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

    def set_subscription_account(self, subscription: str = None) -> dict:
        """Sets the subscription that we wanth the RBAC to be created for.

        ### Parameters
        ----
        subscription_name : str (optional, Default=None)
            Your Azure subscription name or ID. If nothing is provided
            then your azure subscription ID is used when you initialized
            the client.

        ### Returns
        ----
        dict:
            A message specifying whether the operation was successful
            or not.
        """

        if not subscription:
            subscription = self.subscription_id

        self.az_cli.invoke(
            args=['account', 'set', '--subscription', subscription],
            initial_invocation_data=None
        )

        if self.az_cli.result.result == None:
            return {"message": f"Azure Subscription set to {subscription}."}
        elif self.az_cli.result.error:
            return {"message": "Azure operation failed."}

    def create_rbac(self, rbac_name: str, subscription: str = None) -> dict:
        """Creats a new role based service principal using the Azure CLI.

        ### Parameters
        ----
        rbac_name : str
            The name you want your RBAC object to be.

        subscription : str (optional, Default=None)
            Your Azure subscription name or ID. If nothing is provided
            then your azure subscription ID is used when you initialized
            the client.

        ### Returns
        ----
        dict:
            A `RBAC` resource.
        """

        # Step 1: Set the `AzureSubscription` account.
        self.set_subscription_account(
            subscription=subscription
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

    def generate_config_files(self, file_name: Union[str, pathlib.Path]) -> None:
        """Generate a config.ini file where we can store our RBAC Credentials.

        ### Parameters
        ----
        file_name : Union[str, pathlib.Path]
            The location you want to store the config.ini
            file.
        """

        # Load the RBAC Config.
        with open(file="config/azure_rbac_auth_sp.json", mode='r') as rbac_file:
            rbac_config = json.load(fp=rbac_file)

        # Initialize the Parser.
        config = ConfigParser()

        # Add the Section.
        config.add_section('rbac_credentials')

        # Set the Values.
        config.set('rbac_credentials', 'client_id', rbac_config['clientId'])
        config.set('rbac_credentials', 'tenant_id', rbac_config['tenantId'])
        config.set('rbac_credentials', 'client_secret', rbac_config['clientSecret'])
        config.set('rbac_credentials', 'subscription_id', rbac_config['subscriptionId'])

        # Write the file.
        with open(file=file_name, mode='w+') as f:
            config.write(fp=f)

    def generate_batch_script(self, file_name: Union[str, pathlib.Path]) -> None:
        """Generate a .cmd file to set your environment variables
        for Azure.

        ### Parameters
        ----
        file_name : Union[str, pathlib.Path]
            The location you want to store the .cmd
            file.
        """

        # Load the RBAC Config.
        with open(file="config/azure_rbac_auth_sp.json", mode='r') as rbac_file:
            rbac_config = json.load(fp=rbac_file)

        # Write the Command File.
        with open(file=file_name, mode='w+') as cmd_file:

            cmd_file.write(textwrap.dedent("""
            REM Sets the Environment Variables that persist over sessions.
            REM Make sure to run this as an administrator and then shut down VS Code
            REM and re-open it.\n
            """))

            cmd_file.write(f"SETX AZURE_SUBSCRIPTION_ID {rbac_config['subscriptionId']}\n")
            cmd_file.write(f"SETX AZURE_TENANT_ID {rbac_config['tenantId']}\n")
            cmd_file.write(f"SETX AZURE_CLIENT_ID {rbac_config['clientId']}\n")
            cmd_file.write(f"SETX AZURE_CLIENT_SECRET {rbac_config['clientSecret']}")

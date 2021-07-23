import json
from azure.cli.core import get_default_cli
import subprocess


class RoleBasedAccessControl():

    def __init__(self) -> None:
        """Initializes the `RoleBasedAccessControl` object that will be used to
        create a new RBAC role for the trading system."""

        self.dump_file = open('azure_cli.txt', 'w+')
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
            out_file=self.dump_file
        )

        if self.az_cli.result.result == None:
            return {"message": f"Azure Subscription set to {subscription_name}."}
        elif self.az_cli.result.error:
            return {"message": "Azure operation failed."}

        # az account set --subscription azure-data-migration
        # az ad sp create-for-rbac --name SigmaCodingServicePrincipalAuth --skip-assignment --sdk-auth > azure_sigma_auth_sp.json

    def create_rbac(self, subscription_name: str, rbac_name: str) -> dict:
        """[summary]

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

        # Step 2: Define the arguments for creating a new RBAC.
        arguments = [
            'ad', 'sp', 'create-for-rbac', '--name',
            rbac_name, '--skip-assignment', '--sdk-auth',
            '>', 'azure_auth_sp.json'
        ]

        # Step 3: Invoke the operation.
        self.az_cli.invoke(
            args=arguments,
            initial_invocation_data=None,
            out_file=self.dump_file
        )

        if self.az_cli.result.result:
            return self.az_cli.result.result
        elif self.az_cli.result.error:
            return {"message": "Azure operation failed."}

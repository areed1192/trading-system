from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import ResourceNotFoundError


class TradingFactoryStorageClient():

    def __init__(self, trading_sys_client: object) -> None:
        """Initializes the TradingFactoryStorageClient, which can be
        used to manage Azure storage resources.

        ### Arguments:
        ----
        trading_sys_client (object): 
            A `TradingSystemClient` with Azure Credentials.
        """

        from tradesys.client import TradingSystem
        self._trading_system: TradingSystem = trading_sys_client
        self._management_client = None

    @property
    def management_client(self) -> StorageManagementClient:
        """Provides access to the `StorageManagementClient`.

        ### Returns:
        ----
        StorageManagementClient:
            An authorized instance of the `StorageManagementClient``.
        """

        # Define a new Storage Management Client.
        mgmt_client = StorageManagementClient(
            credential=self._trading_system.credentials_client.azure_credentials,
            subscription_id=self._trading_system.credentials_client.subscription_id
        )

        self._management_client = mgmt_client

        return self._management_client

    def does_exist(self, resource_group_name: str, account_name: str) -> bool:
        """Determines whether the given resource exists in the specified resource
        group.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        account_name (str):
            The name of the storage account within the specified resource
            group. Storage account names must be between 3 and 24 characters
            in length and use numbers and lower-case letters only.

        ### Returns:
        ----
        bool:
            `True` if the resource exists, `False` otherwise.
        """

        try:
            storage_dict = self.management_client.storage_accounts.get_properties(
                resource_group_name=resource_group_name,
                account_name=account_name
            ).as_dict()

            if 'id' in storage_dict:
                return True

        except ResourceNotFoundError:
            return False

    def setup(self, resource_group_name: str, account_name: str) -> None:
        """Creates a new Azure Storage Account.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        account_name (str):
            The name of the storage account within the specified resource
            group. Storage account names must be between 3 and 24 characters
            in length and use numbers and lower-case letters only.
        """

        if not self.does_exist(resource_group_name=resource_group_name, account_name=account_name):

            # Setup the template.
            STORAGE_TEMPLATE = self._trading_system.templates_client.load_template(
                'storage_account'
            )

            # Create the Storage Account.
            create_operation = self.management_client.storage_accounts.begin_create(
                resource_group_name=resource_group_name,
                account_name=account_name,
                parameters=STORAGE_TEMPLATE
            )

            # Save the response.
            self._trading_system.templates_client.save_response(
                file_name='storage_account',
                response_dict=create_operation.result().as_dict()
            )

    def delete(self, resource_group_name: str, account_name: str) -> None:
        """Deletes a Azure Storage Account.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        account_name (str):
            The name of the storage account within the specified resource
            group. Storage account names must be between 3 and 24 characters
            in length and use numbers and lower-case letters only.
        """

        if self.does_exist(resource_group_name=resource_group_name, account_name=account_name):

            # Create the Storage Account.
            self.management_client.storage_accounts.delete(
                resource_group_name=resource_group_name,
                account_name=account_name
            )

            response = {
                'message': f'Storage Account {account_name} deleted successfully.'
            }

        else:

            response = {
                'message': f'Storage Account {account_name} does not exist.'
            }

        return response

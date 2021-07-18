from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.core.exceptions import ResourceNotFoundError


class TradingFactoryManagementClient():

    def __init__(self, trading_sys_client: object) -> None:
        """Initializes the `TradingFactoryManagementClient`, which can be
        used to manage Azure Data Factory resources.

        ### Arguments:
        ----
        trading_sys_client (object): 
            A `TradingSystemClient` with Azure Credentials.
        """

        from tradesys.client import TradingSystem
        self._trading_system: TradingSystem = trading_sys_client
        self._management_client = None

    @property
    def management_client(self) -> DataFactoryManagementClient:
        """Provides access to the `DataFactoryManagementClient`.

        ### Returns:
        ----
        DataFactoryManagementClient:
            An authorized instance of the `DataFactoryManagementClient``.
        """

        # Define a new KeyVaultManagement Client.
        data_factory_client = DataFactoryManagementClient(
            credential=self._trading_system.credentials_client.azure_credentials,
            subscription_id=self._trading_system.credentials_client.subscription_id
        )

        self._management_client = data_factory_client

        return self._management_client

    def does_exist(self, resource_group_name: str, factory_name: str) -> bool:
        """Determines whether the given resource exists in the specified resource
        group.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        factory_name (str):
            The data factory name.

        ### Returns:
        ----
        bool:
            `True` if the resource exists, `False` otherwise.
        """

        try:
            vault_dict = self.management_client.factories.get(
                resource_group_name=resource_group_name,
                factory_name=factory_name
            )
            if 'id' in vault_dict.as_dict():
                return True

        except ResourceNotFoundError:
            return False

    def setup(self, resource_group_name: str, factory_name: str) -> None:
        """Creates a new Azure Data Factory resource in the designated resource group
        with the specificed name.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        factory_name (str):
            Name of the data factory.
        """

        if not self.does_exist(resource_group_name=resource_group_name, factory_name=factory_name):

            # Setup the template.
            FACTORY_TEMPLATE = self._trading_system.templates_client.load_template(
                'data_factory'
            )

            # Create the Key Vault.
            create_operation = self.management_client.factories.create_or_update(
                resource_group_name=resource_group_name,
                factory_name=factory_name,
                factory=FACTORY_TEMPLATE
            )

            # Save the response.
            self._trading_system.templates_client.save_response(
                file_name='factory',
                response_dict=create_operation.as_dict()
            )

    def delete(self, resource_group_name: str, factory_name: str) -> None:
        """Deletes an Azure Data Factory

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        factory_name (str):
            Name of the data factory.
        """

        if self.does_exist(resource_group_name=resource_group_name, factory_name=factory_name):

            self.management_client.factories.delete(
                resource_group_name=resource_group_name,
                factory_name=factory_name
            )

            response = {
                'message': f'Azure Data Factory {factory_name} deleted.'
            }

        else:
            response = {
                'message': f'Azure Data Factory {factory_name} does not exist.'
            }

        return response

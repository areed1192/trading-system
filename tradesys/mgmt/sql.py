from azure.mgmt.sql import SqlManagementClient
from azure.core.exceptions import ResourceNotFoundError


class TradingFactorySqlClient():

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
    def management_client(self) -> SqlManagementClient:
        """Provides access to the `SqlManagementClient`.

        ### Returns:
        ----
        SqlManagementClient:
            An authorized instance of the `SqlManagementClient``.
        """

        # Define a new SQL Management Client.
        mgmt_client = SqlManagementClient(
            credential=self._trading_system.credentials_client.azure_credentials,
            subscription_id=self._trading_system.credentials_client.subscription_id
        )

        self._management_client = mgmt_client

        return self._management_client

    def does_exist(self, resource_group_name: str, server_name: str = None, database_name: str = None) -> dict:
        """Determines whether the given resource exists in the specified resource
        group.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        server_name (str): (optional, Default=None)
            The name of the server.

        database_name (str): (optional, Default=None)
            The name of the database.

        ### Returns:
        ----
        dict:
            A response message specifiying whether the resource exists
            or not.
        """

        response = {
            'server_resource': {
                'message': 'Resource not checked.',
                'does_exist': None
            },
            'database_resource': {
                'message': 'Resource not checked.',
                'does_exist': None
            }
        }

        if server_name:

            try:
                server_dict = self.management_client.servers.get(
                    resource_group_name=resource_group_name,
                    server_name=server_name
                ).as_dict()

                if 'id' in server_dict:
                    response['server_resource'][
                        'message'] = f'Server Resource {server_name}, exists.'
                    response['server_resource']['does_exist'] = True

            except ResourceNotFoundError:
                response['server_resource'][
                    'message'] = f'Server Resource {server_name}, doest not exist.'
                response['server_resource']['does_exist'] = False

        if database_name:

            try:
                server_dict = self.management_client.databases.get(
                    resource_group_name=resource_group_name,
                    server_name=server_name,
                    database_name=database_name
                ).as_dict()

                if 'id' in server_dict:
                    response['database_resource'][
                        'message'] = f'Database Resource {database_name}, exists.'
                    response['database_resource']['does_exist'] = True

            except ResourceNotFoundError:
                response['database_resource'][
                    'message'] = f'Database Resource {database_name}, doest not exist.'
                response['database_resource']['does_exist'] = False

        return response

    def setup_server(self, resource_group_name: str, server_name: str) -> None:
        """Creates a new Azure SQL Server.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        server_name (str): (optional, Default=None)
            The name of the server.
        """

        if not self.does_exist(resource_group_name=resource_group_name, server_name=server_name)['server_resource']['does_exist']:

            # Setup the template.
            SERVER_TEMPLATE = self._trading_system.templates_client.load_template(
                'server'
            )

            # Create the Storage Account.
            create_operation = self.management_client.servers.begin_create_or_update(
                resource_group_name=resource_group_name,
                server_name=server_name,
                parameters=SERVER_TEMPLATE
            )

            # Save the response.
            self._trading_system.templates_client.save_response(
                file_name='server',
                response_dict=create_operation.result().as_dict()
            )

    def delete_server(self, resource_group_name: str, server_name: str) -> None:
        """Deletes a Azure SQL Server.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        server_name (str): (optional, Default=None)
            The name of the server.
        """

        if self.does_exist(resource_group_name=resource_group_name, server_name=server_name)['server_resource']['does_exist']:

            # Create the Storage Account.
            self.management_client.servers.begin_delete(
                resource_group_name=resource_group_name,
                server_name=server_name
            )

            response = {
                'message': f'Server Instance {server_name} deleted successfully.'
            }

        else:

            response = {
                'message': f'Server Instance {server_name} does not exist.'
            }

        return response

    def setup_database(self, resource_group_name: str, server_name: str, database_name: str) -> None:
        """Creates a new instance of an Azure SQL database that can be used by the Trading System.

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        server_name (str): (optional, Default=None)
            The name of the server.

        database_name (str): (optional, Default=None)
            The name of the database.
        """

        does_exist_response = self.does_exist(
            resource_group_name=resource_group_name,
            server_name=server_name,
            database_name=database_name
        )

        if not does_exist_response['database_resource']['does_exist']:

            # Setup the template.
            DATABASE_TEMPLATE = self._trading_system.templates_client.load_template(
                'database'
            )

            # Create the Storage Account.
            create_operation = self.management_client.databases.begin_create_or_update(
                resource_group_name=resource_group_name,
                server_name=server_name,
                database_name=database_name,
                parameters=DATABASE_TEMPLATE
            )

            # Save the response.
            self._trading_system.templates_client.save_response(
                file_name='database',
                response_dict=create_operation.result().as_dict()
            )

    def delete_database(self, resource_group_name: str, server_name: str, database_name: str) -> None:
        """Deletes a Azure SQL Database in the specified Server Instance..

        ### Arguments:
        ----
        resource_group_name (str):
            The name of the resource group within the user's subscription.
            The name is case insensitive.

        server_name (str): (optional, Default=None)
            The name of the server.

        database_name (str): (optional, Default=None)
            The name of the database.
        """

        does_exist_response = self.does_exist(
            resource_group_name=resource_group_name,
            server_name=server_name,
            database_name=database_name
        )

        if does_exist_response['database_resource']['does_exist']:

            # Create the Storage Account.
            self.management_client.databases.begin_delete(
                resource_group_name=resource_group_name,
                server_name=server_name,
                database_name=database_name
            )

            response = {
                'message': f'Database Instance {server_name} deleted successfully.'
            }

        else:

            response = {
                'message': f'Database Instance {server_name} does not exist.'
            }

        return response

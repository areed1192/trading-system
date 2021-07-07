from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import ResourceNotFoundError


class TradingFactoryStorage():

    def __init__(self, trading_sys_client: object) -> None:

        from tradesys.client import TradingSystem
        self._trading_system: TradingSystem = trading_sys_client
        self._management_client = None

    @property
    def management_client(self) -> StorageManagementClient:

        # Define a new Storage Management Client.
        mgmt_client = StorageManagementClient(
            credential=self._trading_system.credentials_client.azure_credentials,
            subscription_id=self._trading_system.credentials_client.subscription_id
        )

        self._management_client = mgmt_client

        return self._management_client

    def does_exist(self, resource_group_name: str, account_name: str) -> bool:

        try:
            storage_dict = self.management_client.storage_accounts.get_properties(
                resource_group_name=resource_group_name,
                account_name=account_name
            )

            if 'id' in storage_dict:
                return True

        except ResourceNotFoundError:
            return False

    def setup(self, resource_group_name: str, account_name: str) -> None:

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

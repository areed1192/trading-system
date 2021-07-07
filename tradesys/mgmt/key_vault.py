from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.core.exceptions import ResourceNotFoundError

class TradingFactoryKeyVault():

    def __init__(self, trading_sys_client: object) -> None:

        from tradesys.client import TradingSystem
        self._trading_system: TradingSystem = trading_sys_client
        self._management_client = None

    @property
    def management_client(self) -> KeyVaultManagementClient:

        # Define a new KeyVaultManagement Client.
        key_vault_client = KeyVaultManagementClient(
            credential=self._trading_system.credentials_client.azure_credentials,
            subscription_id=self._trading_system.credentials_client.subscription_id
        )

        self._management_client = key_vault_client

        return self._management_client
    
    def does_exist(self, resource_group_name: str, vault_name: str) -> bool:

        try:
            vault_dict = self.management_client.vaults.get(
                resource_group_name=resource_group_name,
                vault_name=vault_name
            )
            if 'id' in vault_dict.as_dict():
                return True

        except ResourceNotFoundError:
            return False


    def setup(self, resource_group_name: str, value_name: str) -> None:

        if not self.does_exist(resource_group_name=resource_group_name, vault_name=value_name,):

            # Setup the template.
            KEY_VAULT_TEMPLATE = self._trading_system.templates_client.load_template('key_vault')
            KEY_VAULT_TEMPLATE['properties']['tenant_id'] = self._trading_system.credentials_client.tenant_id
            KEY_VAULT_TEMPLATE['properties']['access_policies'][0]['tenant_id'] = self._trading_system.credentials_client.tenant_id

            # Create the Key Vault.
            create_operation = self.management_client.vaults.begin_create_or_update(
                resource_group_name=resource_group_name,
                vault_name=value_name,
                parameters=KEY_VAULT_TEMPLATE
            )

            # Save the response.
            self._trading_system.templates_client.save_response(
                file_name='key_vault',
                response_dict=create_operation.result().as_dict()
            )



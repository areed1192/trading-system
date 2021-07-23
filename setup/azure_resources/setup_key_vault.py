from configparser import ConfigParser
from tradesys.client import TradingSystem
from azure.keyvault.secrets import SecretClient

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Grab the Azure Credentials needed.
iex_api_key = config.get('iex', 'api-key')
sql_connection_string = config.get('sql', 'connection-string')
blob_storage_connectiong_string = config.get(
    'blob_storage',
    'connection-string'
)

# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the `KeyVaultManagementClient`.
vault_mgmt_client = trading_system_client.vault_mgmt_client

# Set some constants.
CREATE_KEY_VAULT = False
UPDATE_ACCESS_POLICY = False

# Step 1: Load our `KeyVault` resource template.
key_vault_resource_template = trading_system_client.templates_client.load_template(
    'key_vault'
)

# Step 2: Set some of the template properties.
key_vault_properties = key_vault_resource_template['properties']
key_vault_properties['tenant_id'] = trading_system_client.credentials_client.tenant_id
key_vault_properties['access_policies'][0]['tenant_id'] = trading_system_client.credentials_client.tenant_id

# Step 3: Create our `AzureKeyVault` resource.
if CREATE_KEY_VAULT:

    # Run the `CreateOrUpdate` opertaion.
    create_vault_operation = vault_mgmt_client.vaults.begin_create_or_update(
        resource_group_name='azure-data-migration',
        vault_name='azure-migration-vault',
        parameters=key_vault_resource_template
    )


# Step 4: Update the `AccessPolicy` for our `AzureKeyVault` so that our Data Factory can read it.
if UPDATE_ACCESS_POLICY:

    # Run the `UpdateAccessPolicy` operation.
    create_access_policy_operation = vault_mgmt_client.vaults.update_access_policy(
        resource_group_name='azure-data-migration',
        vault_name='azure-migration-vault',
        operation_kind='add',
        parameters={
            "properties": {
                "accessPolicies": [
                    {
                        "tenantId": "adacdae5-3dcd-4f38-9749-fb447d12e560",
                        "objectId": "7ab0d1e3-ddd5-4baf-a10b-25a6e232f516",
                        "permissions": {
                            "keys": [
                                "get",
                                "list"
                            ],
                            "secrets": [
                                "set",
                                "get",
                                "list"
                            ]
                        }
                    }
                ]
            }
        }
    )


# Step 5: Grab our new `AzureKeyVault` resource.
key_vault = vault_mgmt_client.vaults.get(
    resource_group_name='azure-data-migration',
    vault_name='azure-migration-vault'
)

# Step 6: Define a new `SecretClient` so we can upload secrets.
secret_client = SecretClient(
    vault_url=key_vault.properties.vault_uri,
    credential=trading_system_client.credentials_client.azure_credentials
)

# Step 7: Set our IEX API Key.
secret_client.set_secret(
    name='iex-api-key',
    value=iex_api_key
)

# Step 8: Set our SQL Connection String.
secret_client.set_secret(
    name='sql-database-connection-string',
    value=sql_connection_string
)

# Step 9: Set our Azure Blob Connection String.
secret_client.set_secret(
    name='azure-blob-connection-string',
    value=blob_storage_connectiong_string
)

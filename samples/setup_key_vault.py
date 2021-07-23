from pprint import pprint
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

# Grab the Key Vault Management Client.
vault_mgmt_client = trading_system_client.vault_mgmt_client

# Set some constants.
CREATE_KEY_VAULT = False
UPDATE_ACCESS_POLICY = False

# Step 1: Create our `AzureKeyVault` resource.
if CREATE_KEY_VAULT:

    vault_mgmt_client.setup(
        resource_group_name='azure-data-migration',
        vault_name='azure-migration-vault'
    )

# Get our Key Vault.
key_vault = vault_mgmt_client.management_client.vaults.get(
    resource_group_name='azure-data-migration',
    vault_name='azure-migration-vault'
)

# Step 2: Update the `AccessPolicy` for our Key Vault so that our Data Factory can read it.
if UPDATE_ACCESS_POLICY:

    # update the access policy so we can add a secret.
    vault_mgmt_client.management_client.vaults.update_access_policy(
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

# Step 3: Define a new `SecretClient` so we can upload secrets.
secret_client = SecretClient(
    vault_url=key_vault.properties.vault_uri,
    credential=trading_system_client.credentials_client.azure_credentials
)

# Step 4: Set our IEX API Key.
secret_client.set_secret(
    name='iex-api-key',
    value=iex_api_key
)

# Step 5: Set our SQL Connection String.
secret_client.set_secret(
    name='sql-database-connection-string',
    value=sql_connection_string
)

# Step 6: Set our Azure Blob Connection String.
secret_client.set_secret(
    name='azure-blob-connection-string',
    value=blob_storage_connectiong_string
)

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

# Step 1: Grab our new `AzureKeyVault` resource.
key_vault = vault_mgmt_client.vaults.get(
    resource_group_name='azure-data-migration',
    vault_name='azure-migration-vault'
)

# Step 2: Define a new `SecretClient` so we can upload secrets.
secret_client = SecretClient(
    vault_url=key_vault.properties.vault_uri,
    credential=trading_system_client.credentials_client.azure_credentials
)

# Step 2: Set our IEX API Key.
secret_client.set_secret(
    name='iex-api-key',
    value=iex_api_key
)

# Step 3: Set our SQL Connection String.
secret_client.set_secret(
    name='sql-database-connection-string',
    value=sql_connection_string
)

# Step 4: Set our Azure Blob Connection String.
secret_client.set_secret(
    name='azure-blob-connection-string',
    value=blob_storage_connectiong_string
)

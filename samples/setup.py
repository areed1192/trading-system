import json
from configparser import ConfigParser
from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.storage import StorageManagementClient


# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Grab the Azure Credentials needed.
subscription_id = config.get('azure_subscriptions', 'azure-data-migration')
tenant_id = config.get('rbac_credentials', 'TENANT_ID')
client_id = config.get('rbac_credentials', 'CLIENT_ID')
client_secret = config.get('rbac_credentials', 'CLIENT_SECRET')

# Create our Credentials.
credential = DefaultAzureCredential()

storage_mgmt_client = StorageManagementClient(
    credential=credential,
    subscription_id=subscription_id
)

# operation_result = storage_mgmt_client.storage_accounts.begin_create(
#     resource_group_name='',
#     account_name='',
# )

# # Define a new KeyVaultManagement Client.
# key_vault_client = KeyVaultManagementClient(
#     credential=credential,
#     subscription_id=subscription_id
# )

# # Define the Authorization Managment Client.
# auth_mgmt_client = AuthorizationManagementClient(
#     credential=credential,
#     subscription_id=subscription_id
# )

# print(key_vault_client.vaults.get(
#     resource_group_name='azure-data-migration',
#     vault_name='azure-migration-vault'
# ))

# # Load the template.
# with open(file='tradesys/templates/key_vault.jsonc', mode='r') as key_vault_template:

#     KEY_VAULT_TEMPLATE = json.load(fp=key_vault_template)
#     KEY_VAULT_TEMPLATE['properties']['tenant_id'] = tenant_id
#     KEY_VAULT_TEMPLATE['properties']['access_policies'][0]['tenant_id'] = tenant_id

# # Create the new key vault.
# create_operation = key_vault_client.vaults.begin_create_or_update(
#     resource_group_name='azure-data-migration',
#     vault_name='azure-migration-vault',
#     parameters=KEY_VAULT_TEMPLATE
# )

# with open(file='tradesys/responses/key_vault.json', mode='w+') as key_vault_json:

#     # Grab the results, and store them.
#     data = create_operation.result().as_dict()
#     json.dump(fp=key_vault_json, obj=data, indent=3)

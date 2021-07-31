from tradesys.client import TradingSystem

# Import LinkedService Models.
from azure.mgmt.datafactory.models import LinkedServiceResource
from azure.mgmt.datafactory.models import LinkedServiceReference
from azure.mgmt.datafactory.models import RestServiceLinkedService
from azure.mgmt.datafactory.models import AzureKeyVaultLinkedService
from azure.mgmt.datafactory.models import AzureKeyVaultSecretReference
from azure.mgmt.datafactory.models import AzureSqlDatabaseLinkedService
from azure.mgmt.datafactory.models import AzureBlobStorageLinkedService
from azure.mgmt.datafactory.models import RestServiceAuthenticationType

RESOURCE_GROUP_NAME = 'azure-data-migration'
DATA_FACTORY_NAME = 'trading-factory'

# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the data Factory Management Client.
data_factory_mgmt_client = trading_system_client.factory_mgmt_client

#########################################
# LINKED SERVICES - AZURE KEY VAULT
#########################################

# Step 1: Define a AzureKeyVaultLinkedService Object.
azure_key_vault_linked_service = AzureKeyVaultLinkedService(
    description='Represents a Azure Key Vault service created for our trading system.',
    base_url='https://azure-migration-vault.vault.azure.net/'
)

# Step 2: Define the Generic LinkedServiceResource.
azure_key_vault_linked_service_resource = LinkedServiceResource(
    properties=azure_key_vault_linked_service
)

# Step 3: Create the LinkedService for our Azure Key Vault.
response = data_factory_mgmt_client.linked_services.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    linked_service_name='TradingSystemKeyVault',
    linked_service=azure_key_vault_linked_service_resource
)

if 'id' in response:
    print('AZURE KEY VAULT LINKED SERVICE CREATED...')

#########################################
# LINKED SERVICES - AZURE SQL DATABASE
#########################################

# Step 1: Create a LinkedServiceReference, to KeyVault.
azure_key_vault_reference = LinkedServiceReference(
    reference_name='TradingKeyVault'
)

# Step 2: Reference a Secret that is inside of our KeyVault.
azure_key_vault_secref_ref = AzureKeyVaultSecretReference(
    secret_name='sql-database-connection-string',
    store=azure_key_vault_reference

)

# Step 3: Define the generic LinkedServiceResource for our Azure SQL Database.
sql_database_linked_service = LinkedServiceResource(
    properties=AzureSqlDatabaseLinkedService(
        description='Represents a SQL Server Database instance that is used to store data for our trading system.',
        connection_string=azure_key_vault_secref_ref
    )
)

# Step 4: Create the LinkedService for our Azure SQL Database.
response = data_factory_mgmt_client.linked_services.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    linked_service_name='TradingSystemSqlDatabase',
    linked_service=sql_database_linked_service
)

if 'id' in response:
    print('AZURE SQL DATABASE LINKED SERVICE CREATED...')

#########################################
# LINKED SERVICES - REST SERVICE
#########################################

# Step 1: Define a RestServiceLinkedService Object.
rest_linked_service = RestServiceLinkedService(
    url='https://cloud.iexapis.com/stable/',
    description='Represents a REST API Service we can use to pull data from the IEX API.',
    enable_server_certificate_validation=True,
    authentication_type=RestServiceAuthenticationType.ANONYMOUS
)

# Step 2: Define the LinkedServiceResource.
rest_linked_service_resource = LinkedServiceResource(
    properties=rest_linked_service
)

# Step 3: Create the LinkedService.
response = data_factory_mgmt_client.linked_services.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    linked_service_name='IexApiService',
    linked_service=rest_linked_service_resource
)

if 'id' in response:
    print('REST SERVICE LINKED SERVICE CREATED...')

#########################################
# LINKED SERVICES - BLOB STORAGE
#########################################

# Step 1: Reference a Secret that is inside of our KeyVault.
azure_key_vault_secref_ref = AzureKeyVaultSecretReference(
    secret_name='azure-blob-connection-string',
    store=azure_key_vault_reference

)

# Step 2: Define a AzureBlobStorageLinkedService Object.
azure_blob_linked_service = AzureBlobStorageLinkedService(
    description='Represents a Blob Storage Service that will house different data related to our news articles.',
    connection_string=azure_key_vault_secref_ref
)

# Step 3: Wrap it in a general LinkedServiceResource.
azure_blob_linked_resource = LinkedServiceResource(
    properties=azure_blob_linked_service
)

# Step 4: Create the LinkedService.
response = data_factory_mgmt_client.linked_services.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    linked_service_name='TradingSystemBlobStorage',
    linked_service=azure_blob_linked_resource
)

if 'id' in response:
    print('BLOB STORAGE LINKED SERVICE CREATED...')

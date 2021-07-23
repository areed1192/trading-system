from tradesys.client import TradingSystem

# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the Storage Client.
storage_mgmt_client = trading_system_client.storage_mgmt_client

# Declare some constants, make sure to change me!!
CREATE_STORAGE = False
CREATE_CONTAINERS = False

# Step 1: Load our `AzureStorage` Template.
storage_resource_template = trading_system_client.templates_client.load_template(
    'storage_account'
)

# Step 2: Setup up the `StorageAccount` resource.
if CREATE_STORAGE:

    # Run the `CreateOrUpdate` operation.
    create_storage_account_operation = storage_mgmt_client.storage_accounts.begin_create(
        resource_group_name='azure-data-migration',
        account_name='tradingsystem',
        parameters=storage_resource_template
    )

# Step 3: Create the `BlobContainer` resource.
if CREATE_CONTAINERS:

    # Run the `CreateOrUpdate` operation.
    create_container_operation = storage_mgmt_client.blob_containers.create(
        resource_group_name='azure-data-migration',
        account_name='tradingsystem',
        container_name='iex-data',
        blob_container={}
    )

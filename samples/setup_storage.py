from tradesys.client import TradingSystem

# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the Storage Client.
storage_client = trading_system_client.storage_mgmt_client

# Declare some constants.
CREATE_STORAGE = False
CREATE_CONTAINERS = True

RESOURCE_GROUP_NAME = 'azure-data-migration'
ACCOUNT_NAME = 'tradingsystem'

# Step 1: Setup up the Storage Account.
if CREATE_STORAGE:

    storage_client.setup(
        resource_group_name=RESOURCE_GROUP_NAME,
        account_name=ACCOUNT_NAME
    )

# Step 2: Create the `Container`.
if CREATE_CONTAINERS:

    storage_client.management_client.blob_containers.create(
        resource_group_name=RESOURCE_GROUP_NAME,
        account_name=ACCOUNT_NAME,
        container_name='iex-data',
        blob_container={}
    )

from pickle import FALSE
from tradesys.client import TradingSystem

# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the Storage Client.
storage_client = trading_system_client.storage_mgmt_client

# Declare some constants.
CREATE_STORAGE = False

# Setup a new storage account.
if CREATE_STORAGE:

    storage_client.setup(
        resource_group_name='azure-data-migration',
        account_name='tradingsystem'
    )

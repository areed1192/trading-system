from azure.mgmt import sql
from tradesys.client import TradingSystem

# Initialize our Trading System.
trading_system_client = TradingSystem()

print(
    trading_system_client.vault_mgmt_client.does_exist(
        resource_group_name='azure-data-migration',
        vault_name='azure-migration-vault'
    )
)

# Grab the Storage Management Client.
storage_client = trading_system_client.storage_mgmt_client
delete_first = False

# If it already exists, delete it.
if storage_client.does_exist(resource_group_name='azure-data-migration', account_name='tradingsystem') and delete_first:

    # Delete the Storage Account.
    print("Deleting Storage Account....")
    storage_client.delete(
        resource_group_name='azure-data-migration',
        account_name='tradingsystem'
    )

    # Setup a new storage account.
    print("Creating Storage Account....")
    storage_client.setup(
        resource_group_name='azure-data-migration',
        account_name='tradingsystem'
    )

# Grab the SQL Management Client.
sql_mgmt_client = trading_system_client.sql_mgmt_client
sql_mgmt_client.setup_server(
    resource_group_name='azure-data-migration',
    server_name='sigma-sql-server'
)
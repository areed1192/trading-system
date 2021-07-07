from tradesys.client import TradingSystem

# Initialize our Trading System.
trading_system_client = TradingSystem()

print(
    trading_system_client.key_vault_client.does_exist(
        resource_group_name='azure-data-migration',
        vault_name='azure-migration-vault'
    )
)

# Setup a new storage account.
trading_system_client.storage_client.setup(
    resource_group_name='azure-data-migration',
    account_name='tradingsystem'
)

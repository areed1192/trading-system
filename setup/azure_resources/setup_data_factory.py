from tradesys.client import TradingSystem

# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the `DataFactoryManagementClient`.
factory_mgmt_client = trading_system_client.factory_mgmt_client

# Set some constants.
CREATE_DATA_FACTORY = False

# Step 1: Load the `DataFactory` resource template.
data_factory_resource_template = trading_system_client.templates_client.load_template(
    'data_factory'
)

# Step 2: Create a new `DataFactory` resource.
if CREATE_DATA_FACTORY:

    # Run the `CreateOrUpdate` operation.
    create_data_factory_operation = factory_mgmt_client.factories.create_or_update(
        resource_group_name='azure-data-migration',
        factory_name='trading-factory',
        factory=data_factory_resource_template
    )

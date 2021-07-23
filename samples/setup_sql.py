from configparser import ConfigParser
from tradesys.client import TradingSystem

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Grab the Azure Credentials needed.
sql_username = config.get('sql', 'username')
sql_password = config.get('sql', 'password')

# Initialize the Trading System Client.
trade_sys_client = TradingSystem()

# Access the SQL Management Client.
trade_sys_sql_client = trade_sys_client.sql_mgmt_client

# Set some constants.
CREATE_SERVER = False
CREATE_DATABASE = False

# Step 1: Create the `Server` object.
if CREATE_SERVER:

    trade_sys_sql_client.setup_server(
        resource_group_name='azure-data-migration',
        server_name='sigma-sql-server',
        username=sql_username,
        password=sql_password
    )

# Step 2: Create the `Database` object.
if CREATE_DATABASE:

    trade_sys_sql_client.setup_database(
        resource_group_name='azure-data-migration',
        server_name='sigma-sql-server',
        database_name='trading-data'
    )

# Step 3: Set the `FirewallRules` so that other Azure Resources (Data Factory) can access this database.
trade_sys_sql_client.management_client.firewall_rules.create_or_update(
    resource_group_name='azure-data-migration',
    server_name='sigma-sql-server',
    firewall_rule_name='AllowAllWindowsAzureIps',
    parameters={
        "startIpAddress": "0.0.0.0",
        "endIpAddress": "0.0.0.0"
    }
)

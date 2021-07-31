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
sql_mgmt_client = trade_sys_client.sql_mgmt_client

# Set some constants.
CREATE_SERVER = False
CREATE_DATABASE = False
CREATE_FIREWALL_RULE = False

# Set some constants for resource creation.
SQL_SERVER_USERNAME = 'SOME_USERNAME'
SQL_SERVER_PASSWORD = 'SOME_STRONG_PASSWORD'

# Step 1: Load our `SqlServer` resource template.
sql_server_resource_template = trade_sys_client.templates_client.load_template(
    'server'
)

# Step 2: Load our `SqlServerDatabase` resource template.
sql_database_resource_template = trade_sys_client.templates_client.load_template(
    'database'
)

# Step 3: Create the `SqlServer` resource.
if CREATE_SERVER:

    # Set the username and password.
    sql_server_resource_template['properties']['administratorLogin'] = SQL_SERVER_USERNAME
    sql_server_resource_template['properties']['administratorLoginPassword'] = SQL_SERVER_PASSWORD

    # Run the `CreateOrUpdate` operation.
    create_server_operation = sql_mgmt_client.servers.create_or_update(
        resource_group_name='azure-data-migration',
        server_name='trading-system-sql-server',
        parameters=sql_server_resource_template
    )

# Step 4: Create the `SqlServerDatabase` resource.
if CREATE_DATABASE:

    # Run the `CreateOrUpdate` operation.
    create_database_operation = sql_mgmt_client.databases.create_or_update(
        resource_group_name='azure-data-migration',
        server_name='trading-system-sql-server',
        database_name='trading-system',
        parameters=sql_database_resource_template
    )

# Step 5: Set the `FirewallRules` so that other Azure Resources (Data Factory) can access this database.
if CREATE_FIREWALL_RULE:

    # Run the `CreateOrUpdate` operation.
    create_firewall_operation = sql_mgmt_client.firewall_rules.create_or_update(
        resource_group_name='azure-data-migration',
        server_name='trading-system-sql-server',
        firewall_rule_name='AllowAllWindowsAzureIps',
        parameters={
            "startIpAddress": "0.0.0.0",
            "endIpAddress": "0.0.0.0"
        }
    )

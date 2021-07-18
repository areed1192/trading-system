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

# Create the Server.
if CREATE_SERVER:

    trade_sys_sql_client.setup_server(
        resource_group_name='azure-data-migration',
        server_name='sigma-sql-server',
        username=sql_username,
        password=sql_password
    )

# Create the database.
if CREATE_DATABASE:

    trade_sys_sql_client.setup_database(
        resource_group_name='azure-data-migration',
        server_name='sigma-sql-server',
        database_name='trading-data'
    )

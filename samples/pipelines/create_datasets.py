from tradesys.client import TradingSystem

# Import LinkedService Models.
from azure.mgmt.datafactory.models import LinkedServiceReference

# Import Dataset Models.
from azure.mgmt.datafactory.models import JsonDataset
from azure.mgmt.datafactory.models import DatasetResource
from azure.mgmt.datafactory.models import RestResourceDataset
from azure.mgmt.datafactory.models import AzureSqlTableDataset
from azure.mgmt.datafactory.models import AzureBlobStorageLocation
from azure.mgmt.datafactory.models import DatasetFolder

RESOURCE_GROUP_NAME = 'azure-data-migration'
DATA_FACTORY_NAME = 'trading-factory'

# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the data Factory Management Client.
data_factory_mgmt_client = trading_system_client.factory_mgmt_client

# Define some folders so we can keep our datasets organized.
prices_folder = DatasetFolder(name='prices')
tickers_folder = DatasetFolder(name='tickers')

#########################################
# DATASETS - REST SERVICE (PRICES)
#########################################

# Step 1: Define `LinkedServiceReference` object that refers to our `RestLinkedService`.
iex_api_reference = LinkedServiceReference(
    reference_name='IexApiService'
)

# Step 2: Define `RestResourceDataset` object.
rest_price_dataset = RestResourceDataset(
    description='Grabs the historical prices for the specific ticker symbol using the historical prices endpoint.',
    linked_service_name=iex_api_reference,
    folder=prices_folder,
    parameters={
        'token': {
            'type': 'string'
        },
        'ticker': {
            'type': 'string',
            'defaultValue': 'MSFT'
        }
    },
    relative_url="@concat('stock/', toLower(dataset().ticker), '/chart/ytd?token=', dataset().token)"
)

# Step 3: Create a new `Dataset` object.
response = data_factory_mgmt_client.management_client.datasets.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    dataset_name='IexPricePull',
    dataset=DatasetResource(properties=rest_price_dataset)
)

if 'id' in response:
    print('REST DATASET (PRICE) CREATED...')

#########################################
# DATASETS - REST SERVICE (TICKERS)
#########################################

# Step 1: Define `LinkedServiceReference` object that refers to our `RestLinkedService`.
iex_api_reference = LinkedServiceReference(
    reference_name='IexApiService'
)

# Step 2: Define `RestResourceDataset` object.
rest_tickers_dataset = RestResourceDataset(
    description='Grabs all the Tickers symbols from IEX.',
    linked_service_name=iex_api_reference,
    folder=tickers_folder,
    parameters={
        'token': {
            'type': 'string'
        }
    },
    relative_url="@concat('ref-data/symbols?token=', dataset().token)"
)

# Step 3: Create a new `Dataset` object.
response = data_factory_mgmt_client.management_client.datasets.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    dataset_name='IexTickerPull',
    dataset=DatasetResource(properties=rest_tickers_dataset)
)

if 'id' in response:
    print('REST DATASET (PRICE) CREATED...')

#########################################
# DATASETS - AZURE SQL TABLE (TICKERS)
#########################################

# Step 1: Define `LinkedServiceReference` object that refers to our `AzureSqlDatabaseLinkedService`.
azure_sql_reference = LinkedServiceReference(
    reference_name='TradingSystemSqlDatabase'
)

# Step 2: Define `AzureSqlTableDataset` object.
azure_tickers_table = AzureSqlTableDataset(
    description='Represents a connection the Azure SQL Database containing IEX Ticker info.',
    linked_service_name=azure_sql_reference,
    folder=tickers_folder,
    table_name='[dbo].[iex_tickers]',
    structure=[
        {
            'name': 'symbol',
            'type': 'String'
        },
        {
            'name': 'name',
            'type': 'String'
        },
        {
            'name': 'date',
            'type': 'DateTime'
        },
        {
            'name': 'type',
            'type': 'String'
        },
        {
            'name': 'lei',
            'type': 'String'
        },
        {
            'name': 'iexId',
            'type': 'String'
        },
        {
            'name': 'region',
            'type': 'String'
        },
        {
            'name': 'currency',
            'type': 'String'
        },
        {
            'name': 'isEnabled',
            'type': 'String'
        },
        {
            'name': 'exchange',
            'type': 'String'
        },
        {
            'name': 'exchangeName',
            'type': 'String'
        },
        {
            'name': 'exchangeSuffix',
            'type': 'String'
        },
        {
            'name': 'figi',
            'type': 'String'
        },
        {
            'name': 'cik',
            'type': 'String'
        }
    ]
)

# Step 3: Create a new `Dataset` object.
response = data_factory_mgmt_client.management_client.datasets.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    dataset_name='IexTickerTable',
    dataset=DatasetResource(properties=azure_tickers_table)
)

if 'id' in response:
    print('AZURE SQL DATABASE TICKER TABLE CREATED...')

#########################################
# DATASETS - AZURE SQL TABLE (PRICES)
#########################################

# Step 1: Define `LinkedServiceReference` object that refers to our `AzureSqlDatabaseLinkedService`.
azure_sql_reference = LinkedServiceReference(
    reference_name='TradingSystemSqlDatabase'
)

# Step 2: Define `AzureSqlTableDataset` object.
azure_price_table = AzureSqlTableDataset(
    description='Represents a connection the Azure SQL Database containing the IEX Price History.',
    linked_service_name=azure_sql_reference,
    folder=prices_folder,
    table_name='[dbo].[iex_price]',
    structure=[
        {
            'name': 'close',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        },
        {
            'name': 'high',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        },
        {
            'name': 'low',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        },
        {
            'name': 'open',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        },
        {
            'name': 'symbol',
            'type': 'varchar'
        },
        {
            'name': 'volume',
            'type': 'decimal',
            'precision': 20,
            'scale': 0
        },
        {
            'name': 'id',
            'type': 'varchar'
        },
        {
            'name': 'key',
            'type': 'varchar'
        },
        {
            'name': 'subkey',
            'type': 'varchar'
        },
        {
            'name': 'date',
            'type': 'datetime',
            'precision': 23,
            'scale': 3
        },
        {
            'name': 'updated',
            'type': 'decimal',
            'precision': 38,
            'scale': 0
        },
        {
            'name': 'changeOverTime',
            'type': 'decimal',
            'precision': 10,
            'scale': 0
        },
        {
            'name': 'marketChangeOverTime',
            'type': 'decimal',
            'precision': 10,
            'scale': 0
        },
        {
            'name': 'uClose',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        },
        {
            'name': 'uHigh',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        },
        {
            'name': 'uLow',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        },
        {
            'name': 'uOpen',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        },
        {
            'name': 'uVolume',
            'type': 'decimal',
            'precision': 20,
            'scale': 0
        },
        {
            'name': 'label',
            'type': 'varchar'
        },
        {
            'name': 'change',
            'type': 'decimal',
            'precision': 38,
            'scale': 0
        },
        {
            'name': 'changePercent',
            'type': 'decimal',
            'precision': 15,
            'scale': 4
        }
    ]
)

# Step 3: Create a new `Dataset` object.
response = data_factory_mgmt_client.management_client.datasets.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    dataset_name='IexPriceTable',
    dataset=DatasetResource(properties=azure_price_table)
)

if 'id' in response:
    print('AZURE SQL DATABASE PRICE TABLE CREATED...')

#########################################
# DATASETS - AZURE BLOB STORAGE (PRICES)
#########################################

# Step 1: Define `LinkedServiceReference` object that refers to our `AzureBlobStorage`.
azure_blob_reference = LinkedServiceReference(
    reference_name='TradingSystemBlobStorage'
)

# Step 2: Define an `AzureBlobStorageLocation`.
azure_blob_location = AzureBlobStorageLocation(
    container='price-history',
    description='Represents a location in our Azure Blob Storage account for dumping price data files.',
    folder_path='iex-price-history',
    file_name={
        'value': '@dataset().FileName',
        'type': 'Expression'
    }
)

# Step 3: Define a `JsonDataset`.
azure_blob_dataset = JsonDataset(
    linked_service_name=azure_blob_reference,
    folder=prices_folder,
    location=azure_blob_location,
    parameters={
        'FileName': {
            'type': 'string'
        }
    }
)

# Step 4: Create a new `Dataset` object.
response = data_factory_mgmt_client.management_client.datasets.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    dataset_name='IexPricesDump',
    dataset=DatasetResource(properties=azure_blob_dataset)
)

if 'id' in response:
    print('AZURE BLOB STORAGE (PRICES) DATASET CREATED...')

#########################################
# DATASETS - AZURE BLOB STORAGE (TICKERS)
#########################################

# Step 1: Define `LinkedServiceReference` object that refers to our `AzureBlobStorage`.
azure_blob_reference = LinkedServiceReference(
    reference_name='TradingSystemBlobStorage'
)

# Step 2: Define an `AzureBlobStorageLocation`.
azure_blob_location = AzureBlobStorageLocation(
    container='price-history',
    description='Represents a location in our Azure Blob Storage account for dumping ticker data files.',
    folder_path='iex-ticker-symbols',
    file_name={
        'value': '@dataset().FileName',
        'type': 'Expression'
    }
)

# Step 3: Define a `JsonDataset`.
azure_blob_dataset = JsonDataset(
    linked_service_name=azure_blob_reference,
    folder=tickers_folder,
    location=azure_blob_location,
    parameters={
        'FileName': {
            'defaultValue': 'tickers.json',
            'type': 'string'
        }
    }
)

# Step 4: Create a new `Dataset` object.
response = data_factory_mgmt_client.management_client.datasets.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    dataset_name='IexTickersDump',
    dataset=DatasetResource(properties=azure_blob_dataset)
)

if 'id' in response:
    print('AZURE BLOB STORAGE (TICKERS) DATASET CREATED...')

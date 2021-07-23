from tradesys.client import TradingSystem

# Import Dataset Models.
from azure.mgmt.datafactory.models import DataFlowSink
from azure.mgmt.datafactory.models import DatasetFolder
from azure.mgmt.datafactory.models import DataFlowSource
from azure.mgmt.datafactory.models import MappingDataFlow
from azure.mgmt.datafactory.models import DataFlowResource
from azure.mgmt.datafactory.models import DatasetReference


RESOURCE_GROUP_NAME = 'azure-data-migration'
DATA_FACTORY_NAME = 'trading-factory'

# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the data Factory Management Client.
data_factory_mgmt_client = trading_system_client.factory_mgmt_client

# Define some folders so we can keep our data flows organized.
prices_folder = DatasetFolder(name='prices')
tickers_folder = DatasetFolder(name='tickers')

#########################################
# DATA FLOWS - PRICES
#########################################

# Step 1: Define our `DataFlowSource`.
data_flow_source = DataFlowSource(
    name='LoadPriceFiles',
    dataset=DatasetReference(reference_name='IexPriceDumps')
)

# Step 1: Define our `DataFlowSink`.
data_flow_sink = DataFlowSink(
    name='LoadToPriceTable',
    dataset=DatasetReference(reference_name='IexPriceTable')
)

# Define the Mapping Data Flow.
mapping_data_flow_iex = MappingDataFlow(
    description='Takes the price history data files, cleans them up, and then loads them to our SQL Database price table.',
    folder=prices_folder,
    sources=[data_flow_source],
    sinks=[data_flow_sink],
    script="source(output(\n\t\tchange as double,\n\t\tchangeOverTime as double,\n\t\tchangePercent as double,\n\t\tclose as double,\n\t\tdate as date,\n\t\tfClose as double,\n\t\tfHigh as double,\n\t\tfLow as double,\n\t\tfOpen as double,\n\t\tfVolume as integer,\n\t\thigh as double,\n\t\tid as string,\n\t\tkey as string,\n\t\tlabel as string,\n\t\tlow as double,\n\t\tmarketChangeOverTime as double,\n\t\topen as double,\n\t\tsubkey as string,\n\t\tsymbol as string,\n\t\tuClose as double,\n\t\tuHigh as double,\n\t\tuLow as double,\n\t\tuOpen as double,\n\t\tuVolume as integer,\n\t\tupdated as long,\n\t\tvolume as integer\n\t),\n\tallowSchemaDrift: true,\n\tvalidateSchema: false,\n\tignoreNoFilesFound: false,\n\tdocumentForm: 'documentPerLine') ~> LoadPriceFiles\nLoadPriceFiles sink(allowSchemaDrift: true,\n\tvalidateSchema: false,\n\tinput(\n\t\tclose as decimal(15,4),\n\t\thigh as decimal(15,4),\n\t\tlow as decimal(15,4),\n\t\topen as decimal(15,4),\n\t\tsymbol as string,\n\t\tvolume as decimal(20,0),\n\t\tid as string,\n\t\tkey as string,\n\t\tsubkey as string,\n\t\tdate as timestamp,\n\t\tupdated as decimal(38,0),\n\t\tchangeOverTime as decimal(10,0),\n\t\tmarketChangeOverTime as decimal(10,0),\n\t\tuClose as decimal(15,4),\n\t\tuHigh as decimal(15,4),\n\t\tuLow as decimal(15,4),\n\t\tuOpen as decimal(15,4),\n\t\tuVolume as decimal(20,0),\n\t\tlabel as string,\n\t\tchange as decimal(38,0),\n\t\tchangePercent as decimal(15,4)\n\t),\n\tdeletable:false,\n\tinsertable:true,\n\tupdateable:false,\n\tupsertable:false,\n\tformat: 'table',\n\tskipDuplicateMapInputs: true,\n\tskipDuplicateMapOutputs: true,\n\terrorHandlingOption: 'stopOnFirstError') ~> LoadToPriceTable"
)

# Create a new Pipe line which includes all our activites.
response = data_factory_mgmt_client.management_client.data_flows.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    data_flow_name='LoadAndTransformPrices',
    data_flow=DataFlowResource(properties=mapping_data_flow_iex)
)

if id in response:
    print("DATA FLOW (PRICE) CREATED...")

#########################################
# DATA FLOWS - TICKERS
#########################################

# Step 1: Define our `DataFlowSource`.
data_flow_source = DataFlowSource(
    name='LoadTickerFiles',
    dataset=DatasetReference(reference_name='IexTickersDumps')
)

# Step 1: Define our `DataFlowSink`.
data_flow_sink = DataFlowSink(
    name='LoadToTickerTable',
    dataset=DatasetReference(reference_name='IexTickersTable')
)

# Define the Mapping Data Flow.
mapping_data_flow_iex = MappingDataFlow(
    description='Takes the ticker data files, cleans them up, and then loads them to our SQL Database ticker table.',
    folder=tickers_folder,
    sources=[data_flow_source],
    sinks=[data_flow_sink],
    script="source(output(\n\t\tcik as integer,\n\t\tcurrency as string,\n\t\tdate as date,\n\t\texchange as string,\n\t\texchangeName as string,\n\t\texchangeSuffix as string,\n\t\tfigi as string,\n\t\tiexId as string,\n\t\tisEnabled as boolean,\n\t\tlei as string,\n\t\tname as string,\n\t\tregion as string,\n\t\tsymbol as string,\n\t\ttype as string\n\t),\n\tallowSchemaDrift: true,\n\tvalidateSchema: false,\n\tignoreNoFilesFound: false,\n\tdocumentForm: 'documentPerLine') ~> LoadTickerFile\nLoadTickerFile sink(allowSchemaDrift: true,\n\tvalidateSchema: false,\n\tinput(\n\t\tsymbol as string,\n\t\tname as string,\n\t\tdate as timestamp,\n\t\ttype as string,\n\t\tlei as string,\n\t\tiexId as string,\n\t\tregion as string,\n\t\tcurrency as string,\n\t\tisEnabled as string,\n\t\texchange as string,\n\t\texchangeName as string,\n\t\texchangeSuffix as string,\n\t\tfigi as string,\n\t\tcik as string\n\t),\n\tdeletable:false,\n\tinsertable:true,\n\tupdateable:false,\n\tupsertable:false,\n\tformat: 'table',\n\tskipDuplicateMapInputs: true,\n\tskipDuplicateMapOutputs: true,\n\terrorHandlingOption: 'stopOnFirstError') ~> LoadToTickerTable"
)

# Create a new Pipe line which includes all our activites.
response = data_factory_mgmt_client.management_client.data_flows.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    data_flow_name='LoadAndTransformTickers',
    data_flow=DataFlowResource(properties=mapping_data_flow_iex)
)

if id in response:
    print("DATA FLOW (TICKER) CREATED...")

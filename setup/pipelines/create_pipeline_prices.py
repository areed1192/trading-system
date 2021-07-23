from tradesys.client import TradingSystem
from azure.keyvault.secrets import SecretClient

# Import DataSource Models.
from azure.mgmt.datafactory.models import RestSource
from azure.mgmt.datafactory.models import AzureSqlSource
from azure.mgmt.datafactory.models import DatasetReference


# Import Activity Models.
from azure.mgmt.datafactory.models import WebActivity
from azure.mgmt.datafactory.models import CopyActivity
from azure.mgmt.datafactory.models import LookupActivity
from azure.mgmt.datafactory.models import ActivityPolicy
from azure.mgmt.datafactory.models import ForEachActivity
from azure.mgmt.datafactory.models import ExecuteDataFlowActivity

# Import Activity Models Utilities.
from azure.mgmt.datafactory.models import JsonSink
from azure.mgmt.datafactory.models import Expression
from azure.mgmt.datafactory.models import JsonWriteSettings
from azure.mgmt.datafactory.models import DataFlowReference
from azure.mgmt.datafactory.models import ActivityDependency
from azure.mgmt.datafactory.models import DependencyCondition
from azure.mgmt.datafactory.models import WebActivityAuthentication
from azure.mgmt.datafactory.models import AzureBlobStorageWriteSettings
from azure.mgmt.datafactory.models import ExecuteDataFlowActivityTypePropertiesCompute

# Import Pipeline Models.
from azure.mgmt.datafactory.models import PipelineResource

RESOURCE_GROUP_NAME = 'azure-data-migration'
DATA_FACTORY_NAME = 'trading-factory'


def build_secret_url(resource_group: str, vault_name: str, secret_name: str, vault_client: object):
    """This will help build our Secret URL that will be used in our `GrapApiKey` activity."""

    # Get the vault we need.
    key_vault = vault_client.management_client.vaults.get(
        resource_group_name=resource_group,
        vault_name=vault_name
    )

    # Get the SecretClient.
    secret_client = SecretClient(
        vault_url=key_vault.properties.vault_uri,
        credential=trading_system_client.credentials_client.azure_credentials
    )

    secret_object = secret_client.get_secret(name=secret_name)

    return secret_object.properties.id + '?api-version=7.1'


# Initialize our Trading System.
trading_system_client = TradingSystem()

# Grab the data Factory Management Client.
data_factory_mgmt_client = trading_system_client.factory_mgmt_client

# Construct the Secret URL.
secret_url = build_secret_url(
    resource_group='azure-data-migration',
    vault_name='azure-migration-vault',
    vault_client=trading_system_client.vault_mgmt_client,
    secret_name='iex-api-key'
)

#########################################
# ACTIVITIES - GENERAL
#########################################

# Define the Activity Policy, we will be using this across multiple activites..
activity_policy = ActivityPolicy(
    timeout='7.00:00:00',
    retry=0,
    retry_interval_in_seconds=30,
    secure_output=False,
    secure_input=True
)

#########################################
# ACTIVITIES - WEB
#########################################

# Step 1: Define the Authentication protocol.
web_activity_auth = WebActivityAuthentication(
    type='MSI',
    resource='https://vault.azure.net'
)

# Step 2: Define a `WebActivity` object, note the `activity_policy` and `url`.
web_activity = WebActivity(
    name='GrabApiKey',
    description='Grabs the API Key from my Azure Key Vault.',
    method='GET',
    url=secret_url,
    policy=activity_policy,
    authentication=web_activity_auth
)

if web_activity.validate() == []:
    print('WEB ACTIVITY DEFINED...')

#########################################
# ACTIVITIES - LOOKUP
#########################################

# Step 1: Define the `AzureSqlSource` we want to lookup data from.
azure_sql_source = AzureSqlSource(
    sql_reader_query='SELECT * FROM [iex_ticker];',
    query_timeout='02:00:00',
    partition_option='None'
)

# Step 2: Define the `ActivityDependency` so that we go forward if previous step was successful.
previous_activity_success = ActivityDependency(
    activity=web_activity.name,
    dependency_conditions=[DependencyCondition.SUCCEEDED]
)

# Step 3: Define the `LookupActivity`.
lookup_activity = LookupActivity(
    name='GrabTradingTickers',
    description='Retrieves all the Tickers that we are will be trading.',
    policy=activity_policy,
    depends_on=[previous_activity_success],
    source=azure_sql_source,
    dataset=DatasetReference(reference_name='IexTickersTable'),
    first_row_only=False
)

if lookup_activity.validate() == []:
    print('LOOKUP ACTIVITY DEFINED...')

#########################################
# ACTIVITIES - COPY DATA
#########################################

# Step 1: Define the `RestSource` where we will copy the data from.
rest_source = RestSource(
    http_request_timeout='00:01:40',
    request_interval='00.00:00:00.010',
    request_method='get'
)

# Step 2: Define the `Sink` or the location where we want to dump the data.
json_sink = JsonSink(
    store_settings=AzureBlobStorageWriteSettings(),
    format_settings=JsonWriteSettings(
        file_pattern='setOfObjects'
    )

)

# Step 3: Define a `DatasetReference` for our `Source`.
rest_dataset_reference = DatasetReference(
    reference_name='IexPricePull',
    parameters={
        'token': {
            'value': "@activity('GrabApiKey').output.value",
            'type': 'Expression'
        },
        'ticker': {
            'value': '@item().symbol',
            'type': 'Expression'
        }
    }
)

# Step 4: Define a `DatasetReference` for our `Sink`.
blob_dataset_reference = DatasetReference(
    reference_name='IexPriceDumps',
    parameters={
        'FileName': {
            'value': "@concat(item().symbol,'.json')",
            'type': 'Expression'
        }
    }
)

# Step 5: Define the activity.
copy_activity = CopyActivity(
    name='CapturePriceHistory',
    description='Grabs historical price data for a specific ticker symbol.',
    policy=activity_policy,
    source=rest_source,
    sink=json_sink,
    enable_staging=False,
    inputs=[rest_dataset_reference],
    outputs=[blob_dataset_reference]
)

if copy_activity.validate() == []:
    print('COPY ACTIVITY DEFINED...')

#########################################
# ACTIVITIES - EXECUTE DATA FLOW
#########################################

# Step 1: Define the `ActivityPolicy` for this specific activity.
activity_policy = ActivityPolicy(
    timeout='1.00:00:00',
    retry=0,
    retry_interval_in_seconds=30,
    secure_output=False,
    secure_input=False
)

# Step 2: Define our `DataFlowReference`.
data_flow_reference = DataFlowReference(
    reference_name='LoadAndTransformPrices',
    dataset_parameters={
        'LoadPriceFiles': {
            'FileName': "@concat(item().symbol,'.json')"
        }
    }
)

# Step 3: Define the `ComputeProperties` for the Data Flow Activity.
compute_type = ExecuteDataFlowActivityTypePropertiesCompute(
    compute_type='General',
    core_count=8
)

# Step 4: Define the `ActivityDependency` so that we go forward if previous step was successful.
previous_activity_success = ActivityDependency(
    activity=copy_activity.name,
    dependency_conditions=[DependencyCondition.SUCCEEDED]
)

# Step 5: Define our `ExecuteDataFlowActivity`.
execute_data_flow_activity = ExecuteDataFlowActivity(
    name='LoadFilesToSQL',
    description='Takes the JSON data files in Blob Storage and loads the Data to our SQL Database.',
    policy=activity_policy,
    depends_on=[previous_activity_success],
    data_flow=data_flow_reference,
    compute=compute_type,
    trace_level='Fine'
)

if execute_data_flow_activity.validate() == []:
    print('EXECUTE DATAFLOW ACTIVITY DEFINED...')


#########################################
# ACTIVITIES - FOR EACH
#########################################

# Step 1: Define the `Expression` we will be using to loop through our collection.
collection_expression = Expression(
    value="@activity('GrabTradingTickers').output.value"
)

# Step 2: Define the `ActivityDependency` so that we go forward if previous step was successful.
previous_activity_success = ActivityDependency(
    activity=lookup_activity.name,
    dependency_conditions=[DependencyCondition.SUCCEEDED]
)

# Step 2: Define the `ForEachActivity` and pass through the activities you want to have part of the loop.
for_each_Activity = ForEachActivity(
    name='LoopThroughEachTicker',
    description='Loops through each ticker symbol returned in the query.',
    items=collection_expression,
    depends_on=[previous_activity_success],
    activities=[
        copy_activity,
        execute_data_flow_activity
    ],
)

if for_each_Activity.validate() == []:
    print('FOR EACH ACTIVITY DEFINED...')

#########################################
# PIPELINES - CREATE
#########################################

# Final Step (A): Define a new `PipelineResource` which includes all our activites.
pipeline_resource = PipelineResource(
    activities=[
        web_activity,
        lookup_activity,
        for_each_Activity
    ]
)

# Final Step (B): Create a new `PipelineResource` in our Data Factory.
response = data_factory_mgmt_client.pipelines.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    pipeline_name='IexPrices',
    pipeline=pipeline_resource
)

if response:
    print('PIPELINE CREATED...')

from tradesys.client import TradingSystem
from azure.keyvault.secrets import SecretClient

# Import DataSource Models.
from azure.mgmt.datafactory.models import RestSource
from azure.mgmt.datafactory.models import DatasetReference

# Import Activity Models.
from azure.mgmt.datafactory.models import WebActivity
from azure.mgmt.datafactory.models import CopyActivity
from azure.mgmt.datafactory.models import ActivityPolicy
from azure.mgmt.datafactory.models import ExecuteDataFlowActivity

# Import Activity Models Utilities.
from azure.mgmt.datafactory.models import JsonSink
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
    reference_name='IexTickersPull',
    parameters={
        'token': {
            'value': "@activity('GrabApiKey').output.value",
            'type': 'Expression'
        }
    }
)

# Step 4: Define a `DatasetReference` for our `Sink`.
blob_dataset_reference = DatasetReference(
    reference_name='IexTickersDump',
    parameters={
        'FileName': 'tickers.json'
    }
)

# Step 5: Define the `ActivityDependency` so that we go forward if previous step was successful.
previous_activity_success = ActivityDependency(
    activity=web_activity.name,
    dependency_conditions=[DependencyCondition.SUCCEEDED]
)


# Step 6: Define the activity.
copy_activity = CopyActivity(
    name='CaptureTickers',
    description='Grabs all the Ticker Symbols provided by IEX.',
    policy=activity_policy,
    source=rest_source,
    sink=json_sink,
    depends_on=[previous_activity_success],
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
    reference_name='LoadAndTransformTickers',
    dataset_parameters={
        'LoadTickerFile': {
            'FileName': 'tickers.json'
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
    description='Takes the JSON data files in Blob Storage and loads the data to our SQL Database.',
    policy=activity_policy,
    depends_on=[previous_activity_success],
    data_flow=data_flow_reference,
    compute=compute_type,
    trace_level='Fine'
)

if execute_data_flow_activity.validate() == []:
    print('EXECUTE DATAFLOW ACTIVITY DEFINED...')

#########################################
# PIPELINES - CREATE
#########################################

# Final Step (A): Define a new `PipelineResource` which includes all our activites.
pipeline_resource = PipelineResource(
    activities=[
        web_activity,
        copy_activity,
        execute_data_flow_activity
    ]
)

# Final Step (B): Create a new `PipelineResource` in our Data Factory.
response = data_factory_mgmt_client.management_client.pipelines.create_or_update(
    resource_group_name=RESOURCE_GROUP_NAME,
    factory_name=DATA_FACTORY_NAME,
    pipeline_name='IexTickers',
    pipeline=pipeline_resource
)

if 'id' in response:
    print('PIPELINE CREATED...')

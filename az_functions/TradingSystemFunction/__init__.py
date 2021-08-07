import json
import logging
import azure.functions as func
from .stock_frame.build import StockFrame
from .indicators.build import Indicators
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobServiceClient


def grab_container() -> ContainerClient:
   
    # Initialize the Credentials.
    default_credential = DefaultAzureCredential()

    # Define the URL to our Blob Client Service.
    account_url = 'https://tradingsystem.blob.core.windows.net/'

    # Connect to the client.
    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=default_credential
    )

    # Grab the container.
    container_client = blob_service_client.get_container_client(
        container='price-history'
    )

    return container_client

def clean_json(blob_content: bytes) -> dict:
    """Cleans up the content from Blob Storage, hidden characters present."""

    content: bytes = blob_content.readall()
    json_content = content.decode("unicode_escape").replace("\r\n", ",").replace('ï»¿','')
    proper_json = '[' + json_content[:-1] + ']'

    return json.loads(s=proper_json)

def main(req: func.HttpRequest) -> func.HttpResponse:

    symbol = req.params.get('symbol')
    logging.info(f'Symbol `{symbol}` captured...')

    # Grab the blob content.
    blob_container = grab_container()
    blob_content = blob_container.download_blob(blob='iex-price-history/MSFT.json')
    price_data = clean_json(blob_content=blob_content)
    logging.info('Data Captured Scucessfully...')

    # Prep for indicators.
    stock_frame = StockFrame(data=price_data)
    indicators = Indicators(price_data_frame=stock_frame)

    # Define the indicators.
    indicators.rsi(period=14)
    indicators.sma(period=100)
    indicators.ema(period=50, alpha=1/50)

    stock_frame_with_indicators = indicators.price_data_frame
    price_data = stock_frame_with_indicators.to_dict(orient='records')

    return func.HttpResponse(
        body=json.dumps(obj=price_data, indent=2),
        mimetype='application/json',
        status_code=200
    )

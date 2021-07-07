import pathlib
from configparser import ConfigParser
from azure.identity import DefaultAzureCredential


class TradingCredentials():

    def __init__(self) -> None:

        # Read the file.
        config_folder = pathlib.Path(__file__).parents[2].joinpath('config/')
        config_file = config_folder.joinpath('config.ini')

        self.config = ConfigParser()
        self.config.read(config_file)

        self._subscription_id = None
        self._tenant_id = None
        self._client_id = None
        self._client_secret = None

    @property
    def subscription_id(self) -> str:
        return self.config.get('azure_subscriptions', 'azure-data-migration')

    @property
    def tenant_id(self) -> str:
        return self.config.get('rbac_credentials', 'TENANT_ID')

    @property
    def client_id(self) -> str:
        return self.config.get('rbac_credentials', 'CLIENT_ID')

    @property
    def client_secret(self) -> str:
        return self.config.get('rbac_credentials', 'CLIENT_SECRET')

    @property
    def azure_credentials(self) -> DefaultAzureCredential:
        return DefaultAzureCredential()

    def to_dict(self) -> dict:

        return {
            'tenant_id': self.tenant_id,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'subscription_id': self.subscription_id
        }


if __name__ == '__main__':

    trading_credentials_client = TradingCredentials()
    print(trading_credentials_client.to_dict())

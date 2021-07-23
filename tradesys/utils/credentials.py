import pathlib
from configparser import ConfigParser
from azure.identity import DefaultAzureCredential


class TradingCredentials():

    def __init__(self) -> None:
        """Initializes the `TradingCredentials` object.

        ### Overview
        ----
        This object helps interact with the `DefaultAzureCredential`
        object which will handle authentication of the different Azure
        resources.
        """

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
        """Returns your Azure Subscription ID.

        ### Returns
        ----
        str: 
            Your Azure Subscription ID.
        """

        return self.config.get('azure_subscriptions', 'azure-data-migration')

    @property
    def tenant_id(self) -> str:
        """Returns your Azure Tenant ID.

        ### Returns
        ----
        str: 
            Your Azure Tenant ID.
        """

        return self.config.get('rbac_credentials', 'TENANT_ID')

    @property
    def client_id(self) -> str:
        """Returns your Azure Client ID.

        ### Returns
        ----
        str: 
            Your Azure Client ID.
        """

        return self.config.get('rbac_credentials', 'CLIENT_ID')

    @property
    def client_secret(self) -> str:
        """Returns your Azure Client Secret.

        ### Returns
        ----
        str: 
            Your Azure Client ID.
        """

        return self.config.get('rbac_credentials', 'CLIENT_SECRET')

    @property
    def azure_credentials(self) -> DefaultAzureCredential:
        """Returns the `DefaultAzureCredential` object used for authentication.

        ### Returns
        ----
        DefaultAzureCredential: 
            An non-authenticated instance of the `DefaultAzureCredential`
            object.
        """

        return DefaultAzureCredential()

    def to_dict(self) -> dict:
        """Returns all the properties as a python dictionary.

        ### Returns
        ----
        dict: 
            A dictionary of your azure credentials.
        """

        return {
            'tenant_id': self.tenant_id,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'subscription_id': self.subscription_id
        }

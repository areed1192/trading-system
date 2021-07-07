

class TradingFactoryKeyVault():

    def __init__(self, trading_sys_client: object) -> None:

        from tradesys.client import TradingSystem

        self._trading_system: TradingSystem = trading_sys_client

        # self.key_vault = KeyVaultManagementClient(credential=cred_client, subscription_id=subscription_id)

    def setup_keyvault(self) -> None:
        pass

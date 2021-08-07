import pathlib
from azureml.core import Workspace


class MachineLearningSetup():

    def __init__(self, subscription_id: str, resource_group: str) -> None:

        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self._workspace: Workspace = None
        self.config_folder = pathlib.Path(__file__).parents[2].joinpath('config/')

    def setup_workspace(self, name: str, location: str) -> Workspace:

        trading_ws = Workspace.create(
            name=name,
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            create_resource_group=False,
            location=location
        )

        trading_ws.write_config(
            path=self.config_folder,
            file_name="trading_ws_config.json"
        )

        return trading_ws

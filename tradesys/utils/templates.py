import json
import pathlib


class AzureTemplates():

    def __init__(self) -> None:
        """Initializes the AzureTemplate Utility."""

        main_directory = pathlib.Path(__file__).parents[1]
        self.template_folder = main_directory.joinpath('azure/templates/')
        self.response_folder = main_directory.joinpath('azure/responses/')

    def load_template(self, template_name: str) -> dict:
        """Loads an azure template file.

        ### Parameters
        ----
        template_name : str
            The name of the template file to load.

        ### Returns
        ----
        dict:
            The template file as a dictionary.
        """

        file_name = self.template_folder.joinpath(template_name + '.jsonc')

        with open(file=file_name, mode='r') as temp_file:
            return json.load(fp=temp_file)

    def save_response(self, file_name: str, response_dict: dict) -> pathlib.Path:
        """Saves the response from an Azure Resource Creation step.

        ### Parameters
        ----
        file_name : str
            The name of the new file.

        response_dict :dict
            The response from the create operation.

        ### Returns
        ----
        pathlib.Path:
            The location of the new file.
        """

        file_name = self.response_folder.joinpath(file_name + '.jsonc')

        with open(file=file_name, mode='w+') as temp_file:
            return json.dump(fp=temp_file, obj=response_dict, indent=2)

import json
import pathlib

class AzureTemplates():

    def __init__(self) -> None:

        self.template_folder = pathlib.Path(__file__).parents[1].joinpath('templates/')
        self.response_folder = pathlib.Path(__file__).parents[1].joinpath('responses/')
    
    def load_template(self, template_name: str) -> dict:
        """Loads an azure template file.

        ### Arguments:
        ----
        template_name (str):
            The name of the template file to load.

        ### Returns:
        ----
        dict:
            The template file as a dictionary.
        """        

        file_name = self.template_folder.joinpath(template_name + '.jsonc')

        with open(file=file_name, mode='r') as temp_file:
            return json.load(fp=temp_file)
    
    def save_response(self, file_name: str, response_dict: dict) -> pathlib.Path:

        file_name = self.response_folder.joinpath(file_name + '.jsonc')

        with open(file=file_name, mode='w+') as temp_file:
            return json.dump(fp=temp_file, obj=response_dict, indent=2)

if __name__ == '__main__':

    template_loader = AzureTemplates()
    print(template_loader.template_folder)
    print(template_loader.load_template('key_vault'))
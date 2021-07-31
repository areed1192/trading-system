import pathlib
from tradesys.rbac.client import RoleBasedAccessControl

# Grab your subscription ID, before running this script.
subscription_id = '<YOUR_AZURE_SUBSCRIPTION_ID>'

# Initialize the Client.
rbac_client = RoleBasedAccessControl(subscription_id=subscription_id)

# If we have access to the CLI continue.
if rbac_client.check_for_azure_cli():

    # Then create a new RBAC object.
    print(
        rbac_client.create_rbac(
            subscription_name='azure-data-migration',
            rbac_name='myTestRbac'
        )
    )

    # Create our new config file.
    config_location = pathlib.Path("config/my_new_config.ini")
    rbac_client.generate_config_files(file_name=config_location)

    # Create our new command file.
    script_location = pathlib.Path("config/my_new_script.cmd")
    rbac_client.generate_batch_scripts(file_name=script_location)

    # After these files are generated, make sure to run the new command file.
    # In this case the `my_new_script.cmd` file. On windows all you need to do
    # is just double click it. After you run it, YOU MUST CLOSE DOWN THE TERMINAL
    # AND CLOSE VISUAL STUDIO CODE (NOT RELOAD THE WINDOW)! YOU WON'T BE ABLE TO
    # READ THE NEW ENVIRONMENT VARIABLES UNTIL YOU DO THAT.

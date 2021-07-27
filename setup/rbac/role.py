from tradesys.rbac.client import RoleBasedAccessControl

# Initialize the Client.
rbac_client = RoleBasedAccessControl(subscription_id='')

# If we have access to the CLI continue.
if rbac_client.check_for_azure_cli():

    # Then create a new RBAC object.
    print(
        rbac_client.create_rbac(
            subscription_name='azure-data-migration',
            rbac_name='myTestRbac'
        )
    )

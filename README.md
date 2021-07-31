# Python Trading System

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Support These Projects](#support-these-projects)

## Overview

In this project, you can use python to help develop your own trading system which you can use
to help place and manage trades using the Azure Ecosystem. Not only will this project help setup
your azure services like a data factory, key vault, and sql databases but it will also help get you
started with a few piplines and tables that you can use to store and transform your data.

Along with leveraging Azure Data services, it also helps you leverage Azure Machine learning services where
you can develop machine learning models to help generate signals that can be used for trading purposes.

## Requirements

1.A Microsoft Azure Subscription.
2.The Azure CLI installed on your system.
3.A IEX API Key.
4.A TD Ameritrade Account.

## Setup

**Setup - Requirements Install:**

For this particular project, you only need to install the dependencies, to use the project. The dependencies
are listed in the `requirements.txt` file and can be installed by running the following command:

```console
pip install -r requirements.txt
```

After running that command, the dependencies should be installed.

**Setup - Local Install:**

If you are planning to make modifications to this project or you would like to access it
before it has been indexed on `PyPi`. I would recommend you either install this project
in `editable` mode or do a `local install`. For those of you, who want to make modifications
to this project. I would recommend you install the library in `editable` mode.

If you want to install the library in `editable` mode, make sure to run the `setup.py`
file, so you can install any dependencies you may need. To run the `setup.py` file,
run the following command in your terminal.

```console
pip install -e .
```

If you don't plan to make any modifications to the project but still want to use it across
your different projects, then do a local install.

```console
pip install .
```

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the library wherever you want.

## Usage

Here is a simple example of using the `tradesys` library to create `RoleBasedAccessControl` object.

```python
import pathlib
from tradesys.rbac.client import RoleBasedAccessControl

# Grab your subscription ID, before running this script.
subscription_id = '<YOUR_AZURE_SUBSCRIPTION_ID>'

# Initialize the Client.
rbac_client = RoleBasedAccessControl(subscription_id=subscription_id)

# If we have access to the CLI continue.
if rbac_client.check_for_azure_cli():

    # Then create a new RBAC object.
    print(rbac_client.create_rbac(rbac_name='myTestRbac'))

    # Create our new config file.
    config_location = pathlib.Path("config/my_new_config.ini")
    rbac_client.generate_config_files(file_name=config_location)

    # Create our new command file.
    script_location = pathlib.Path("config/my_new_script.cmd")
    rbac_client.generate_batch_script(file_name=script_location)

```

Here we can see how to create a SQL Server using some of the templates provided:

```python
from tradesys.client import TradingSystem

# Initialize the Trading System Client.
trade_sys_client = TradingSystem()

# Access the SQL Management Client.
sql_mgmt_client = trade_sys_client.sql_mgmt_client

# Set some constants.
CREATE_SERVER = True
CREATE_DATABASE = True
CREATE_FIREWALL_RULE = True

# Set some constants for resource creation.
SQL_SERVER_USERNAME = 'SOME_USERNAME'
SQL_SERVER_PASSWORD = 'SOME_STRONG_PASSWORD'
AZURE_RESOURCE_GROUP = 'YOUR_AZURE_RESOURCE_GROUP'

# Step 1: Load our `SqlServer` resource template.
sql_server_resource_template = trade_sys_client.templates_client.load_template(
    'server'
)

# Step 2: Load our `SqlServerDatabase` resource template.
sql_database_resource_template = trade_sys_client.templates_client.load_template(
    'database'
)

# Step 3: Create the `SqlServer` resource.
if CREATE_SERVER:

    # Set the username and password.
    sql_server_resource_template['properties']['administratorLogin'] = SQL_SERVER_USERNAME
    sql_server_resource_template['properties']['administratorLoginPassword'] = SQL_SERVER_PASSWORD

    # Run the `CreateOrUpdate` operation.
    create_server_operation = sql_mgmt_client.servers.create_or_update(
        resource_group_name=AZURE_RESOURCE_GROUP,
        server_name='trading-system-sql-server',
        parameters=sql_server_resource_template
    )

# Step 4: Create the `SqlServerDatabase` resource.
if CREATE_DATABASE:

    # Run the `CreateOrUpdate` operation.
    create_database_operation = sql_mgmt_client.databases.create_or_update(
        resource_group_name=AZURE_RESOURCE_GROUP,
        server_name='trading-system-sql-server',
        database_name='trading-system',
        parameters=sql_database_resource_template
    )

# Step 5: Set the `FirewallRules` so that other Azure Resources (Data Factory) can access this database.
if CREATE_FIREWALL_RULE:

    # Run the `CreateOrUpdate` operation.
    create_firewall_operation = sql_mgmt_client.firewall_rules.create_or_update(
        resource_group_name=AZURE_RESOURCE_GROUP,
        server_name='trading-system-sql-server',
        firewall_rule_name='AllowAllWindowsAzureIps',
        parameters={
            "startIpAddress": "0.0.0.0",
            "endIpAddress": "0.0.0.0"
        }
    )
```

## Support These Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding). I'm
always looking to add more content for individuals like yourself, unfortuantely some of the APIs I would require me to
pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

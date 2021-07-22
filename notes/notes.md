# Notes Azure Project

General notes

1.When creating the Azure Key Vault, make sure the logged in user has permissions to view secrets.
2.When creating a data factory ensure it has the proper Access Policy for the Key Vault, also set JSON property so it has System Assigned User Identity.
3.When creating a SQL Server, ensure Public Access is on, unless you plan to do a VPN.

```terminal
az sql server show -n sigma-sql-server -g azure-data-migration --query "publicNetworkAccess"
az sql server update -n sigma-sql-server -g azure-data-migration --set publicNetworkAccess="Enabled"
```

-- if you're planning on using managed identity to access the SQL Server
-- you need to create a user that is the data factory and then give it the
-- proper permissions.
CREATE USER [trading-factory] FROM EXTERNAL PROVIDER;

-- Here I'm saying it can write data.
ALTER ROLE db_datawriter ADD MEMBER [trading-factory];
ALTER ROLE db_datareader ADD MEMBER [trading-factory];
ALTER ROLE db_owner ADD MEMBER [trading-factory];


-- HERE ARE OTHER ROLES:
--------------------------------------------
-- DatabaseRoleName         DatabaseUserName
-- db_accessadmin           No members
-- db_backupoperator        No members
-- db_datareader            No members
-- db_datawriter            No members
-- db_ddladmin              No members
-- db_denydatareader        No members
-- db_denydatawriter        No members
-- db_owner                 dbo
-- db_securityadmin         No members
-- dbmanager                No members
-- loginmanager             No members
-- public                   No members
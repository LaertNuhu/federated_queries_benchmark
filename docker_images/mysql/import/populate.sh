#!/bin/bash

# grant priviledges
echo "GRANT ALL PRIVILEGES ON *.* TO 'presto'@'%';" | mysql -u root --password=mysql

# SET GLOBAL local_infile=1;
echo "SET GLOBAL local_infile=1;" | mysql -u root --password=mysql

# Add public database -> if it exists nobody cares
echo "create database public;" | mysql --local-infile=1 -u presto --password=mysql

# create, import, index for sf1
mysql public < /import/create_tpch_sf1.sql --local-infile=1 -u presto --password=mysql
mysql public < /import/indexes_tpch_sf1.sql --local-infile=1 -u presto --password=mysql
mysql public < /import/import_tpch_sf1.sql --local-infile=1 -u presto --password=mysql

# # create, import, index for sf10
# mysql public < /import/create_tpch_sf10.sql --local-infile=1 -u presto --password=mysql
# mysql public < /import/indexes_tpch_sf10.sql --local-infile=1 -u presto --password=mysql
# mysql public < /import/import_tpch_sf10.sql --local-infile=1 -u presto --password=mysql
#!/bin/bash
# This script is intended to be executed on-demand using 'docker exec' to copy
# test data from the local /data directory to HBase.

echo "create 'users','cf'" | $HBASE_HOME/bin/hbase shell -n
echo "create 'orders','cf'" | $HBASE_HOME/bin/hbase shell -n

$HBASE_HOME/bin/hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns='HBASE_ROW_KEY, cf:reg_date, cf:country' users file:///data/users.csv
$HBASE_HOME/bin/hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns='HBASE_ROW_KEY, cf:type, cf:source, cf:photo_id, cf:price, cf:country' orders file:///data/orders.csv
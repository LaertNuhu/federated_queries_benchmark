#!/bin/bash
# This script is intended to be executed on-demand using 'docker exec' to copy
# test data from the local /data directory to HBase.

echo "create 'lineitem', 'cf'" | $HBASE_HOME/bin/hbase shell -n

$HBASE_HOME/bin/hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator='|' -Dimporttsv.columns='HBASE_ROW_KEY, cf:l_partkey, cf:l_suppkey, cf:l_linenumber, cf:l_quantity, cf:l_extendedprice, cf:l_discount, cf:l_tax, cf:l_returnflag, cf:l_linestatus, cf:l_shipdate, cf:l_commitdate, cf:l_receiptdate, cf:l_shipinstruct, cf:l_shipmode, cf:l_comment' lineitem file:///data/lineitem.tbl
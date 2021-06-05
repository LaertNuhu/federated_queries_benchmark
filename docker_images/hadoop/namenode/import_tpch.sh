#!/bin/bash
# This script is intended to be executed on-demand using 'docker exec' to copy
# test data from the local /data directory to HDFS.

$HADOOP_HOME/bin/hdfs dfs -mkdir -p /data
$HADOOP_HOME/bin/hdfs dfs -copyFromLocal /data/part.tbl /data/
$HADOOP_HOME/bin/hdfs dfs -copyFromLocal /data/partsupp.tbl /data/
$HADOOP_HOME/bin/hdfs dfs -copyFromLocal /data/orders.tbl /data/
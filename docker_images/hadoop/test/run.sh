#!/bin/bash

$HADOOP_HOME/bin/hdfs dfs -mkdir -p $INPUT
$HADOOP_HOME/bin/hdfs dfs -copyFromLocal -f /opt/hadoop-${HADOOP_VERSION}/README.txt $INPUT/
$HADOOP_HOME/bin/hadoop jar $JAR_FILEPATH $CLASS_TO_RUN $INPUT $OUTPUT
$HADOOP_HOME/bin/hdfs dfs -cat $OUTPUT/*
cat /opt/hadoop-${HADOOP_VERSION}/README.txt
$HADOOP_HOME/bin/hdfs dfs -rm -r $OUTPUT
$HADOOP_HOME/bin/hdfs dfs -rm -r $INPUT
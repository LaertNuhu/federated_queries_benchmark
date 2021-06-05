#!/bin/bash

export SPARK_MASTER_HOST=`hostname`

source "$SPARK_HOME/sbin/spark-config.sh"
source "$SPARK_HOME/bin/load-spark-env.sh"

mkdir -p $SPARK_LOG

ln -sf /dev/stdout $SPARK_LOG/spark-master.out

$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master \
    --host $SPARK_MASTER_HOST \
    --port $SPARK_MASTER_PORT \
    --webui-port $SPARK_MASTER_WEBUI_PORT \
    >> $SPARK_LOG/spark-master.out
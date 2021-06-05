#!/bin/bash

source "$SPARK_HOME/sbin/spark-config.sh"
source "$SPARK_HOME/bin/load-spark-env.sh"

mkdir -p $SPARK_LOG

ln -sf /dev/stdout $SPARK_LOG/spark-worker.out

$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker \
    --webui-port $SPARK_WORKER_WEBUI_PORT \
    $SPARK_MASTER \
    >> $SPARK_LOG/spark-worker.out
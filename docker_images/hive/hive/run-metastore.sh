#!/bin/bash

$HIVE_HOME/bin/schematool -dbType postgres -initSchema
$HIVE_HOME/bin/hive --service metastore
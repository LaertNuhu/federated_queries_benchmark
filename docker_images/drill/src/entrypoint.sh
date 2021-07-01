#!/bin/bash

DRILL_OVERRIDE_CONF=${DRILL_HOME}/conf/drill-override.conf
DRILL_EXEC_OPTIONS_PREFIX=DRILL_EXEC_

set_zookeeper_host() {
    sed -i "s/zk.*/zk.connect: \"${1}\"/g" ${DRILL_OVERRIDE_CONF}
}

set_exec_options() {

    DRILL_EXEC_OPTIONS=$(printenv | grep "^${DRILL_EXEC_OPTIONS_PREFIX}.*$" | wc -l)

    if [[ "${DRILL_EXEC_OPTIONS}" > "0" ]]; then

        echo 'drill.exec.options: {' >> ${DRILL_OVERRIDE_CONF}

        DRILL_CONFIGS=$(printenv | grep "^${DRILL_EXEC_OPTIONS_PREFIX}.*$" | awk -F= '{print $1}')
        for config_name in ${DRILL_CONFIGS}; do
            config_key=$(echo ${config_name:${#DRILL_EXEC_OPTIONS_PREFIX}} | sed 's/_/./g' | awk '{print tolower($0)}')
            config_value=$(printenv ${config_name})
            echo "    ${config_key}: ${config_value}" >> ${DRILL_OVERRIDE_CONF}
        done

        echo '}' >> ${DRILL_OVERRIDE_CONF}
    fi
}

start_embedded() {
    echo 'Starting in embedded mode...'
    ${DRILL_HOME}/bin/drill-embedded
}

start_cluster() {
    echo 'Starting in clustered mode...'
    ${DRILL_HOME}/bin/drillbit.sh run
}

sed -i "s/export DRILLBIT_OPTS=\"-Xms.*/export DRILLBIT_OPTS=\"-XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap -XX:MaxRAMFraction=${HEAP_MEMORY_FRACTION:-2}\"/g" ${DRILL_HOME}/bin/drill-config.sh

set_exec_options

if [[ -n "${CLUSTERED_MODE}" && "${CLUSTERED_MODE}" == "true" ]]; then
    if [[ -n "${ZOOKEEPER_HOST}" ]]; then
        echo "Zookeeper host configured at ${ZOOKEEPER_HOST}, updating configuration..."
        set_zookeeper_host ${ZOOKEEPER_HOST}
    fi
    start_cluster
else
    start_embedded
fi

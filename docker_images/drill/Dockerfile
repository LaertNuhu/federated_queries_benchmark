FROM apache/drill:1.18.0

LABEL maintainer="robvadai"
LABEL github="https://github.com/segence-docker/drill"

ENV DRILL_HOME=/opt/drill
ENV DRILL_USER=drill

COPY src/logback.xml ${DRILL_HOME}/conf/
COPY src/entrypoint.sh /

RUN useradd --home-dir ${DRILL_HOME} --comment 'Drill user' ${DRILL_USER}
RUN chown -R ${DRILL_USER}:${DRILL_USER} ${DRILL_HOME} && chown ${DRILL_USER}:${DRILL_USER} /entrypoint.sh

COPY jars/* ${DRILL_HOME}/jars/3rdparty/
COPY create_plugins.sh /

RUN chmod +x create_plugins.sh

USER ${DRILL_USER}

WORKDIR ${DRILL_HOME}

RUN chmod +x /entrypoint.sh

ENTRYPOINT /entrypoint.sh
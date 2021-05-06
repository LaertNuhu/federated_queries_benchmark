FROM apache/drill:1.18.0
EXPOSE 8047

COPY postgresql-42.2.11.jar /opt/drill/jars/3rdparty/
COPY configs /configs
COPY create_plugins.sh /

RUN chmod +x create_plugins.sh
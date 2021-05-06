FROM hadoop-base

HEALTHCHECK CMD curl -f http://localhost:9870/ || exit 1

ENV HDFS_CONF_dfs_namenode_name_dir file:///hadoop/dfs/name

RUN mkdir -p /hadoop/dfs/name
VOLUME /hadoop/dfs/name

COPY run.sh /run.sh
RUN chmod a+x /run.sh

COPY import_tpch.sh /import_tpch.sh
RUN chmod a+x /import_tpch.sh

EXPOSE 9870

CMD ["/run.sh"]
FROM polydb/hbase-base

COPY run.sh /run.sh
RUN chmod a+x /run.sh

COPY import_python.sh /import_python.sh
RUN chmod a+x /import_python.sh

COPY import_tpch.sh /import_tpch.sh
RUN chmod a+x /import_tpch.sh

EXPOSE 16000 16010

CMD ["/run.sh"]
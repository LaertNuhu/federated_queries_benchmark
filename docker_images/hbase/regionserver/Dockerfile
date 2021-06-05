FROM polydb/hbase-base

COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 16020 16030

CMD ["/run.sh"]
FROM polydb/hadoop-base

ENV HBASE_VERSION 2.2.6
ENV HBASE_URL https://dist.apache.org/repos/dist/release/hbase/$HBASE_VERSION/hbase-$HBASE_VERSION-bin.tar.gz
ENV HBASE_HOME /opt/hbase-$HBASE_VERSION
ENV HBASE_CONF_DIR /etc/hbase
ENV PATH $HBASE_HOME/bin/:$PATH

RUN curl -O https://dist.apache.org/repos/dist/release/hbase/KEYS
RUN gpg --import KEYS

RUN set -x \
    && curl -fSL "$HBASE_URL" -o /tmp/hbase.tar.gz \
    && curl -fSL "$HBASE_URL.asc" -o /tmp/hbase.tar.gz.asc \
    && gpg --verify /tmp/hbase.tar.gz.asc \
    && tar -xvf /tmp/hbase.tar.gz -C /opt/ \
    && rm /tmp/hbase.tar.gz*

RUN ln -s /opt/hbase-$HBASE_VERSION/conf /etc/hbase

RUN mkdir /opt/hbase-$HBASE_VERSION/logs

COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
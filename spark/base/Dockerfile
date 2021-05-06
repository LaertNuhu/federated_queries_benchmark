FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV SPARK_VERSION=2.2.3
#ENV SPARK_VERSION=3.1.1
ENV HADOOP_VERSION=2.7
#ENV SPARK_URL https://dist.apache.org/repos/dist/release/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
ENV SPARK_URL https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
ENV SPARK_HOME /opt/spark
ENV USER root
ENV PATH $SPARK_HOME/bin/:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-8-jdk \
        net-tools \
        curl \
        netcat \
        gnupg \
        libsnappy-dev \
    && rm -rf /var/lib/apt/lists/*

#RUN curl -O https://dist.apache.org/repos/dist/release/spark/KEYS
#RUN gpg --import KEYS

RUN set -x \
    && curl -fSL "$SPARK_URL" -o /tmp/spark.tgz \
#    && curl -fSL "$SPARK_URL.asc" -o /tmp/spark.tgz.asc \
#    && gpg --verify /tmp/spark.tgz.asc \
    && tar -xvzf /tmp/spark.tgz -C /opt/ \
    && mv /opt/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION /opt/spark \
    && rm /tmp/spark.tgz*

COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
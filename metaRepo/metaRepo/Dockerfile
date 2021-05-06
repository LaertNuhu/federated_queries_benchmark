FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-8-jdk \
        net-tools \
        curl \
        netcat \
        gnupg \
        libsnappy-dev \
        git \
        maven \
    && rm -rf /var/lib/apt/lists/*

COPY code /metaRepo
COPY config.properties /metaRepo/src/main/resources/
COPY application.properties /metaRepo/src/main/resources/
RUN cd /metaRepo \
    && mvn clean package

COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 8181

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/run.sh"]
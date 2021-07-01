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

RUN update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

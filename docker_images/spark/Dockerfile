FROM docker.io/bitnami/spark:2

USER root
RUN curl https://jdbc.postgresql.org/download/postgresql-42.2.22.jar --output /opt/bitnami/spark/jars/postgresql.jar
RUN curl https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.25/mysql-connector-java-8.0.25.jar --output /opt/bitnami/spark/jars/mysql.jar
RUN pip install findspark

USER 1001

FROM mariadb:10.5-focal

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt install openjdk-8-jdk -y && export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
RUN apt-get remove --purge mariadb-server-10.5 -y && apt-get autoremove -y && apt-get autoclean -y
RUN apt-get update && apt-get install mariadb-server-10.5 mariadb-plugin-connect -y
RUN apt-get update && apt-get install libodbc1 unixodbc-dev libssl-dev odbc-postgresql curl alien -y

# comment out a few problematic configuration values
RUN	find /etc/mysql/ -name '*.cnf' -print0 \
		| xargs -0 grep -lZE '^(bind-address|log|user\s)' \
		| xargs -rt -0 sed -Ei 's/^(bind-address|log|user\s)/#&/';
# don't reverse lookup hostnames, they are usually another container
RUN	echo '[mysqld]\nskip-host-cache\nskip-name-resolve' > /etc/mysql/conf.d/docker.cnf

#RUN apt-get update && apt-get install software-properties-common mariadb-plugin-connect -y
RUN curl -O https://downloads.cloudera.com/connectors/hive_odbc_2.6.1.1001/Linux/ClouderaHiveODBC-2.6.1.1001-1.x86_64.rpm
RUN alien -i ClouderaHiveODBC-2.6.1.1001-1.x86_64.rpm
COPY config/hive.ini /
RUN cat hive.ini >> /etc/odbcinst.ini

#https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/2.7.7/hadoop-common-2.7.7.jar
#https://repo1.maven.org/maven2/org/apache/hive/hive-jdbc/2.3.8/hive-jdbc-2.3.8-standalone.jar
#https://repo.hortonworks.com/content/repositories/releases/org/apache/hive/hive-jdbc/2.3.8/hive-jdbc-2.3.8.jar
#https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-auth/2.7.7/hadoop-auth-2.7.7.jar
#https://downloads.cloudera.com/connectors/ClouderaHiveJDBC-2.6.13.1016.zip

COPY ./jars/* /usr/lib/mysql/plugin/
COPY ./lib/* /tmp/
COPY ./connect.cnf /etc/mysql/mariadb.conf.d/connect.cnf
RUN chmod 0444 /etc/mysql/mariadb.conf.d/connect.cnf
COPY privileges.sql /docker-entrypoint-initdb.d/

COPY import/create_tpch_sf1.sql /create_tpch_sf1.sql
COPY import/import_tpch_sf1.sql /import_tpch_sf1.sql
COPY import/indexes_tpch_sf1.sql /indexes_tpch_sf1.sql


VOLUME /var/lib/mysql

EXPOSE 3306

CMD ["mysqld"]
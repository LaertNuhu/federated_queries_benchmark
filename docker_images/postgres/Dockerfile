FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc-dev \
        make \
        cmake \
        ca-certificates \
        git \
        postgresql-12 \
        postgresql-server-dev-12 \
        odbc-postgresql \
        unixodbc-dev \
        libssl-dev \
        alien \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/CartoDB/odbc_fdw.git && cd odbc_fdw && make && make install

RUN git clone https://github.com/MariaDB/mariadb-connector-odbc.git
RUN mkdir build && cd build && cmake ../mariadb-connector-odbc/ -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCONC_WITH_UNIT_TESTS=Off -DCMAKE_INSTALL_PREFIX=/usr/local -DWITH_SSL=OPENSSL \
    && cmake --build . --config RelWithDebInfo \
    && make install

COPY config/mariadb.ini /
RUN cat mariadb.ini >> /etc/odbcinst.ini

RUN curl -O https://downloads.cloudera.com/connectors/hive_odbc_2.6.1.1001/Linux/ClouderaHiveODBC-2.6.1.1001-1.x86_64.rpm
RUN alien -i ClouderaHiveODBC-2.6.1.1001-1.x86_64.rpm
COPY config/hive.ini /
RUN cat hive.ini >> /etc/odbcinst.ini

USER postgres

RUN    /etc/init.d/postgresql start &&\
    psql --command "ALTER USER postgres WITH PASSWORD '123456';" &&\
    createdb -O postgres db1

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/12/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/12/main/postgresql.conf

EXPOSE 5432

COPY import/create_tpch_sf1.sql /create_tpch_sf1.sql
COPY import/import_tpch_sf1.sh /import_tpch_sf1.sh

COPY import/create_tpch_sf10.sql /create_tpch_sf10.sql
COPY import/import_tpch_sf10.sh /import_tpch_sf10.sh


VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

CMD ["/usr/lib/postgresql/12/bin/postgres", "-D", "/var/lib/postgresql/12/main", "-c", "config_file=/etc/postgresql/12/main/postgresql.conf"]
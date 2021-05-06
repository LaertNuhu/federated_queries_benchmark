#!/bin/sh

set +x && \
sed "s\CREATE TABLE pg_\CREATE TABLE pg$1_\g" create_tpch_sf10.sql >/tmp/create10.sql && \
psql -f /tmp/create10.sql db1 && \
psql -d db1 -c "\copy pg$1_sf10_lineitem FROM /data/sf10/lineitem.tbl with CSV DELIMITER '|' QUOTE '\"' ESCAPE '\';" && \
psql -d db1 -c "\copy pg$1_sf10_supplier FROM /data/sf10/supplier.tbl with CSV DELIMITER '|' QUOTE '\"' ESCAPE '\';" && \
psql -d db1 -c "\copy pg$1_sf10_region FROM /data/sf10/region.tbl with CSV DELIMITER '|' QUOTE '\"' ESCAPE '\';" && \
psql -d db1 -c "\copy pg$1_sf10_nation FROM /data/sf10/nation.tbl with CSV DELIMITER '|' QUOTE '\"' ESCAPE '\';" && \
psql -d db1 -c "\copy pg$1_sf10_orders FROM /data/sf10/orders.tbl with CSV DELIMITER '|' QUOTE '\"' ESCAPE '\';" && \
psql -d db1 -c "\copy pg$1_sf10_customer FROM /data/sf10/customer.tbl with CSV DELIMITER '|' QUOTE '\"' ESCAPE '\';" && \
psql -d db1 -c "\copy pg$1_sf10_partsupp FROM /data/sf10/partsupp.tbl with CSV DELIMITER '|' QUOTE '\"' ESCAPE '\';" && \
psql -d db1 -c "\copy pg$1_sf10_part FROM /data/sf10/part.tbl with CSV DELIMITER '|' QUOTE '\"' ESCAPE '\';"
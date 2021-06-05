LOAD DATA LOCAL INFILE '/data/sf10/customer.tbl' into table mysql_sf10_customer FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf10/orders.tbl' into table mysql_sf10_orders FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf10/lineitem.tbl' into table mysql_sf10_lineitem FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf10/nation.tbl' into table mysql_sf10_nation FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf10/partsupp.tbl' into table mysql_sf10_partsupp FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf10/part.tbl' into table mysql_sf10_part FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf10/region.tbl' into table mysql_sf10_region FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf10/supplier.tbl' into table mysql_sf10_supplier FIELDS TERMINATED BY '|';
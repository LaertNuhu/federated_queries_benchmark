LOAD DATA LOCAL INFILE '/data/sf1/customer.tbl' into table mysql_sf1_customer FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf1/orders.tbl' into table mysql_sf1_orders FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf1/lineitem.tbl' into table mysql_sf1_lineitem FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf1/nation.tbl' into table mysql_sf1_nation FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf1/partsupp.tbl' into table mysql_sf1_partsupp FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf1/part.tbl' into table mysql_sf1_part FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf1/region.tbl' into table mysql_sf1_region FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE '/data/sf1/supplier.tbl' into table mysql_sf1_supplier FIELDS TERMINATED BY '|';
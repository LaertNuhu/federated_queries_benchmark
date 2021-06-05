USE tpch;
LOAD DATA LOCAL INPATH '/data/sf1/nation.tbl' OVERWRITE INTO TABLE hive_sf1_nation;
LOAD DATA LOCAL INPATH '/data/sf1/region.tbl' OVERWRITE INTO TABLE hive_sf1_region;
LOAD DATA LOCAL INPATH '/data/sf1/part.tbl' OVERWRITE INTO TABLE hive_sf1_part;
LOAD DATA LOCAL INPATH '/data/sf1/supplier.tbl' OVERWRITE INTO TABLE hive_sf1_supplier;
LOAD DATA LOCAL INPATH '/data/sf1/partsupp.tbl' OVERWRITE INTO TABLE hive_sf1_partsupp;
LOAD DATA LOCAL INPATH '/data/sf1/customer.tbl' OVERWRITE INTO TABLE hive_sf1_customer;
LOAD DATA LOCAL INPATH '/data/sf1/orders.tbl' OVERWRITE INTO TABLE hive_sf1_orders;
LOAD DATA LOCAL INPATH '/data/sf1/lineitem.tbl' OVERWRITE INTO TABLE hive_sf1_lineitem;


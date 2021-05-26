ALTER TABLE mysql_sf10_part
    ADD CONSTRAINT part_kpey
        PRIMARY KEY (p_partkey);

ALTER TABLE mysql_sf10_supplier
    ADD CONSTRAINT supplier_pkey
        PRIMARY KEY (s_suppkey);

ALTER TABLE mysql_sf10_partsupp
    ADD CONSTRAINT partsupp_pkey
        PRIMARY KEY (ps_partkey, ps_suppkey);

ALTER TABLE mysql_sf10_customer
    ADD CONSTRAINT customer_pkey
        PRIMARY KEY (c_custkey);

ALTER TABLE mysql_sf10_orders
    ADD CONSTRAINT orders_pkey
        PRIMARY KEY (o_orderkey);

ALTER TABLE mysql_sf10_lineitem
    ADD CONSTRAINT lineitem_pkey
        PRIMARY KEY (l_orderkey, l_linenumber);

ALTER TABLE mysql_sf10_nation
    ADD CONSTRAINT nation_pkey
        PRIMARY KEY (n_nationkey);

ALTER TABLE mysql_sf10_region
    ADD CONSTRAINT region_pkey
        PRIMARY KEY (r_regionkey);
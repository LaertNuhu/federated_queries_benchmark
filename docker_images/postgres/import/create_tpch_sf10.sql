CREATE TABLE pg_sf10_supplier
(
    s_suppkey   INTEGER,
    s_name      CHAR(25),
    s_address   VARCHAR(40),
    s_nationkey INTEGER,
    s_phone     CHAR(15),
    s_acctbal   NUMERIC(20, 2),
    s_comment   VARCHAR(101)
);

CREATE TABLE pg_sf10_part
(
    p_partkey     INTEGER,
    p_name        VARCHAR(55),
    p_mfgr        CHAR(25),
    p_brand       CHAR(10),
    p_type        VARCHAR(25),
    p_size        INTEGER,
    p_container   CHAR(10),
    p_retailprice NUMERIC(20, 2),
    p_comment     VARCHAR(23)
);

CREATE TABLE pg_sf10_partsupp
(
    ps_partkey    INTEGER,
    ps_suppkey    INTEGER,
    ps_availqty   INTEGER,
    ps_supplycost NUMERIC(20, 2),
    ps_comment    VARCHAR(199)
);

CREATE TABLE pg_sf10_customer
(
    c_custkey    INTEGER,
    c_name       VARCHAR(25),
    c_address    VARCHAR(40),
    c_nationkey  INTEGER,
    c_phone      CHAR(15),
    c_acctbal    NUMERIC(20, 2),
    c_mktsegment CHAR(10),
    c_comment    VARCHAR(117)
);

CREATE TABLE pg_sf10_orders
(
    o_orderkey      BIGINT,
    o_custkey       INTEGER,
    o_orderstatus   CHAR(1),
    o_totalprice    NUMERIC,
    o_orderdate     DATE,
    o_orderpriority CHAR(15),
    o_clerk         CHAR(15),
    o_shippriority  INTEGER,
    o_comment       VARCHAR(79)
);

CREATE TABLE pg_sf10_lineitem
(
    l_orderkey      BIGINT,
    l_partkey       INTEGER,
    l_suppkey       INTEGER,
    l_linenumber    INTEGER,
    l_quantity      NUMERIC(20, 2),
    l_extendedprice NUMERIC(20, 2),
    l_discount      NUMERIC(3, 2),
    l_tax           NUMERIC(3, 2),
    l_returnflag    CHAR(1),
    l_linestatus    CHAR(1),
    l_shipdate      DATE,
    l_commitdate    DATE,
    l_receiptdate   DATE,
    l_shipinstruct  CHAR(25),
    l_shipmode      CHAR(10),
    l_comment       VARCHAR(44)
);

CREATE TABLE pg_sf10_nation
(
    n_nationkey INTEGER,
    n_name      CHAR(25),
    n_regionkey INTEGER,
    n_comment   VARCHAR(152)
);

CREATE TABLE pg_sf10_region
(
    r_regionkey INTEGER,
    r_name      CHAR(25),
    r_comment   VARCHAR(152)
);

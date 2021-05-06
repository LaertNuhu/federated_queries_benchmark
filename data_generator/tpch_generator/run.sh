#!/bin/bash

cd /tpch-dbgen

./dbgen -vf -T O -s 1
./dbgen -vf -T P -s 1
./dbgen -vf -T S -s 1
./dbgen -vf -T L -s 1
./dbgen -vf -T c -s 1
./dbgen -vf -T n -s 1
./dbgen -vf -T r -s 1
./dbgen -vf -T s -s 1

mkdir -p /data/sf1
mv orders.tbl /data/sf1/orders.tbl
mv part.tbl /data/sf1/part.tbl
mv partsupp.tbl /data/sf1/partsupp.tbl
mv lineitem.tbl /data/sf1/lineitem.tbl
mv customer.tbl /data/sf1/customer.tbl
mv nation.tbl /data/sf1/nation.tbl
mv region.tbl /data/sf1/region.tbl
mv supplier.tbl /data/sf1/supplier.tbl

./dbgen -vf -T O -s 10
./dbgen -vf -T P -s 10
./dbgen -vf -T S -s 10
./dbgen -vf -T L -s 10
./dbgen -vf -T c -s 10
./dbgen -vf -T n -s 10
./dbgen -vf -T r -s 10
./dbgen -vf -T s -s 10

mkdir -p /data/sf10
mv orders.tbl /data/sf10/orders.tbl
mv part.tbl /data/sf10/part.tbl
mv partsupp.tbl /data/sf10/partsupp.tbl
mv lineitem.tbl /data/sf10/lineitem.tbl
mv customer.tbl /data/sf10/customer.tbl
mv nation.tbl /data/sf10/nation.tbl
mv region.tbl /data/sf10/region.tbl
mv supplier.tbl /data/sf10/supplier.tbl

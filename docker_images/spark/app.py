import findspark
import re
findspark.init() 
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
import socket

def run_query(sql):
    sql = __parse_sql(sql)
    spark = get_spark_context("benchmark")

def __parse_sql(sql):
    pattern = re.compile("(\w*.public.\w*)")
    return pattern.sub(lambda m: m.group().replace('.',"_"), sql)

def get_spark_context(app_name: str) -> SparkSession:
    """
    Helper to manage the `SparkContext` and keep all of our
    configuration params in one place. See below comments for details:
        |_ https://github.com/bitnami/bitnami-docker-spark/issues/18#issuecomment-700628676
        |_ https://github.com/leriel/pyspark-easy-start/blob/master/read_file.py
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    conf = SparkConf()
    conf.setAll(
        [
            (
                "spark.master",
                "spark://spark-master:7077",
            ),
            ("spark.driver.host", ip_address),
            ("spark.submit.deployMode", "client"),
            ("spark.driver.bindAddress", "0.0.0.0"),
            ("spark.app.name", app_name),
            ("spark.jars", "/opt/bitnami/spark/jars/postgresql.jar"),
            ("spark.jars","/opt/bitnami/spark/jars/mysql.jar"),
            ("spark.executor.memory", "10g")
        ]
    )

    return SparkSession.builder.config(conf=conf).getOrCreate()


if __name__ == "__main__":

    # Regular Spark job executed on a Docker container
    spark = get_spark_context("employees")
    spark.read.format("jdbc").option(
        "url", "jdbc:postgresql://pg-1:5432/benchmark"
        ).option(
            "fetchSize","250000"
        ).option(
            "numPartitions", "8"
        ).option(
            "dbtable", "postgress_sf1_lineitem"
        ).option(
            "user","benchmark"
        ).option(
            "password", "secret123"
        ).option(
            "driver", "org.postgresql.Driver"
        ).load().createTempView("lineitem")
    spark.read.format("jdbc").option(
        "url", "jdbc:postgresql://pg-2:5432/benchmark"
        ).option(
            "fetchSize","250000"
        ).option(
            "numPartitions", "8"
        ).option(
            "dbtable", "postgress_sf1_customer"
        ).option(
            "user","benchmark"
        ).option(
            "password", "secret123"
        ).option(
            "driver", "org.postgresql.Driver"
        ).load().createTempView("postgress2_public_customer")
    spark.read.format("jdbc").option(
        "url", "jdbc:postgresql://pg-3:5432/benchmark"
        ).option(
            "fetchSize","250000"
        ).option(
            "numPartitions", "8"
        ).option(
            "dbtable", "postgress_sf1_orders"
        ).option(
            "user","benchmark"
        ).option(
            "password", "secret123"
        ).option(
            "driver", "org.postgresql.Driver"
        ).load().createTempView("orders")
    spark.read.format("jdbc").option(
        "url", "jdbc:postgresql://pg-1:5432/benchmark"
        ).option(
            "fetchSize","250000"
        ).option(
            "numPartitions", "8"
        ).option(
            "dbtable", "postgress_sf1_nation"
        ).option(
            "user","benchmark"
        ).option(
            "password", "secret123"
        ).option(
            "driver", "org.postgresql.Driver"
        ).load().createTempView("nation")
    result = spark.sql("-- TPC-H Query 10\n\nselect\n        c_custkey,\n        c_name,\n        sum(l_extendedprice * (1 - l_discount)) as revenue,\n        c_acctbal,\n        n_name,\n        c_address,\n        c_phone,\n        c_comment\nfrom\n        postgress2_public_customer,\n        orders,\n        lineitem,\n        nation\nwhere\n        c_custkey = o_custkey\n        and l_orderkey = o_orderkey\n        and o_orderdate >= date '1993-10-01'\n        and o_orderdate < date '1994-01-01'\n        and l_returnflag = 'R'\n        and c_nationkey = n_nationkey\ngroup by\n        c_custkey,\n        c_name,\n        c_acctbal,\n        c_phone,\n        n_name,\n        c_address,\n        c_comment\norder by\n        revenue desc\nlimit 20")
    result.show()
    spark.stop()


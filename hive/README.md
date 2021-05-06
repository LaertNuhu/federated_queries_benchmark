# Hive for polydb

*This is a working documentation for the polydb Hive instance.*

In general, you only need to work in this directory if you want to build, run or test Hive in a minimal setup without the other systems in this repo.

### Build
This builds the Hive Docker images based on the Dockerfiles in this directory. You only need to run this if you made changes to one of the Dockerfiles or if you have not built the Hive images yet. In any way, Docker caches your images and will not repeat all of the build steps if you have built the images already.
```
make build
```

### Run
**Note:** Hive depends on Hadoop and therefore, you also need to build the `polydb/hadoop-namenode` and `polydb/hadoop-datanode` images to run the example.
```
docker-compose up
```

### Test
To test Hive, start up the containers and connect to the hive-server using either a locally installed `beeline` client or any other JDBC interface.
```
docker-compose up
beeline -u jdbc:hive2://localhost:10000
```
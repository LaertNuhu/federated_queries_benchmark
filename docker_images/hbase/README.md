# HBase for polydb

*This is a working documentation for the polydb HBase cluster.*

In general, you only need to work in this directory if you want to build, run or test HBase in a minimal setup without the other systems in this repo.

### Build
This builds the HBase Docker images based on the Dockerfiles in this directory. You only need to run this if you made changes to one of the Dockerfiles or if you have not built the HBase images yet. In any way, Docker caches your images and will not repeat all of the build steps if you have built the images already.
```
make build
```

### Run
**Note:** HBase depends on Hadoop and therefore, you also need to build the `polydb/hadoop-namenode` and `polydb/hadoop-datanode` images to run the example.
```
docker-compose up
```

### Test
To test Hbase, start up the containers and run the Hbase shell on the `hbase-master` container.
```
docker-compose up
docker exec -it hbase-master hbase shell
```
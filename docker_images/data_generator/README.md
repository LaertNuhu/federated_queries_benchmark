# polydb data generator

*This is a working documentation for the polydb data generator.*

In general, you only need to work in this directory if you want to build, run or test the data generator in a minimal setup without the other systems in this repo.

### Build
This builds the data generator Docker image based on the Dockerfile in this directory. You only need to run this if you made changes to the Dockerfile or if you have not built the data generator image yet. In any way, Docker caches your images and will not repeat all of the build steps if you have built the images already.

```
make build
```

### Run
**Note:** The data generator example runs with Hadoop and Hbase. Therefore, you also need to build the images in the `hadoop` and `hbase` directories to run the example.

First, start the Docker containers.
```
docker-compose up
```

After the data generator has succefully generated test data and exited (look into the Docker logs), you can copy the data to HDFS and Hbase by running the respective `import_data` scripts.
```
docker exec -it namenode bash /import_data.sh
docker exec -it hbase-master bash /import_data.sh
```
**Note:** As of now, the HBase import only seems to work if you delete all relevant Docker volumes before running `docker-compose`.

### Test
First, executed the steps described in the Run Section. 
To test if the data was generated and imported correctly, check the contents of HDFS and Hbase.

You can access the Hadoop namenode via `localhost:9870`. The connect to Hbase, run the following command:
```
docker exec -it hbase-master hbase shell
```
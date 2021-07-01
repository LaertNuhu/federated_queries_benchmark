# Hadoop cluster for polydb

*This is a working documentation for the Hadoop cluster.*

In general, you only need to work in this directory if you want to build, run or test Hadoop without any of the other systems in this repo.

### Build
This builds the Hadoop Docker images based on the Dockerfiles in this directory. You only need to run this if you made changes to one of the Dockerfiles or if you have not built the Hadoop images yet. In any way, Docker caches your images and will not repeat all of the build steps if you have built the images already.
```
make build
```

### Run
```
docker-compose up
```
**Note:** You may notice that the Resourcemanager fails a couple of times during startup because the Namenode is in _safemode_ and does not allow modifications to the file system. This problem should fix itself since the Namenode automatically leaves _safemode_ after some time and the docker-compose file restarts all components on failure.

### Test
To test the cluster with an example wordcount job, you first need to start up the cluster and then run the test.
```
docker-compose up
make hadoop-test
```
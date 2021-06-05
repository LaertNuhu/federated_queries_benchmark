# Spark cluster for polydb

*This is a working documentation for the Spark cluster.*

In general, you only need to work in this directory if you want to build, run or test Spark without any of the other systems in this repo.

### Build
This builds the Spark Docker images based on the Dockerfiles in this directory. You only need to run this if you made changes to one of the Dockerfiles or if you have not built the Spark images yet. In any way, Docker caches your images and will not repeat all of the build steps if you have built the images already.
```
make build
```

### Run
```
docker-compose up
```

### Test
**TODO**
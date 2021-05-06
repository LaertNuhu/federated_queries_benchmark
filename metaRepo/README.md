# metaRepo for polydb

*This is a working documentation for the polydb metaRepo instance.*

In general, you only need to work in this directory if you want to build, run or test metaRepo in a minimal setup without the other systems in this repo.

### Build
This builds the metaRepo Docker images based on the Dockerfiles in this directory. You only need to run this if you made changes to one of the Dockerfiles or if you have not built the metaRepo images yet. In any way, Docker caches your images and will not repeat all of the build steps if you have built the images already.
```
make build
```
**Todo:** Pull the source code directly from the origin repo in the Dockerfile.

### Run
**Todo**

### Test
**Todo**
# polydb-docker

## Setup
To run polydb-docker, you need `docker` and `docker-compose` installed on your system.
This prototype was tested with Docker 19.03 and docker-compose 1.27 but may work with other versions as well.

To prepare for execution, you need to build all of the necessary containers.
```
make build
```

After building the containers you need to create the test-data docker volume. Run this step only once.

```
make generate-test-data
```

After it is completed you should have a volume named test-data when `docker volume ls` is executed

While test-data is being generated you can already run:
```
make run
``` 
This command will start all the conatiners defined on your docker compose file. 

You should have: 
- jupyter notebook running on `localost:8888` (password is _demo_)
- drill web ui running on `localhost:8047`
- presto web ui running on `localhost:8080`

If another service has the previos mentioned ports occupied, please modify docker-compose file accordingly. 

To populate databases with test-data run:
```
make populate
```
This step is to be executed after `make generate-test-data` command is compleded successfully, and `make run` was already executed.
# polydb-docker

## Setup
To run polydb-docker, you need `docker` and `docker-compose` installed on your system.
This prototype was tested with Docker 19.03 and docker-compose 1.27 but may work with other versions as well.

At first, you need to clone or copy the `metaRepo` repository to the correct location since this is a private repository.
```
git clone https://github.com/spapadop/metaRepo.git metaRepo/metaRepo/code
```

To prepare for execution, you need to build all of the necessary containers.
```
make build
```

## Execution
Run either the Python or TPC-H data generator container to generate a Docker volume with test data.
```
docker run -it --rm -v test-data:/data --env-file data_generator/data_generator.env --name data-generator polydb/python-generator
```
or
```
docker run -it --rm -v test-data:/data --env-file data_generator/data_generator.env --name data-generator polydb/tpch-generator
```

Run `docker-compose` to start all necessary containers.
```
docker-compose up
```

Run the data import scripts for the data generator you used to import data into HDFS and HBase.
```
docker exec -it namenode bash /import_python.sh
docker exec -it hbase-master bash /import_python.sh
```
or
```
docker exec -it namenode bash /import_tpch.sh
docker exec -it hbase-master bash /import_tpch.sh
```

After you imported the test data, call `init` on the metaRepo service.
```
curl -X POST http://localhost:8181/admin/init
```

Enter a shell on the polydb container to run the example jobs.
```
docker exec -it polydb bash
```

Within the polydb shell, you can use predefined aliases to execute jobs.
```
TODO
```

To clean up, shut down `docker-compose` and remove the data generator container and the test data volume.
```
# Use the -v option to remove all docker volumes that were created during the test
docker-compose down -v
docker volume rm test-data
```

POSTGRESS := $(shell docker ps --format '{{.Names}}' --filter name=pg)
MYSQL := $(shell docker ps --format '{{.Names}}' --filter name=mysql)
DRILL := $(shell docker ps --format '{{.Names}}' --filter name=drill)
build:
	$(MAKE) -C data_generator
	# $(MAKE) -C hadoop
	# $(MAKE) -C hbase
	# $(MAKE) -C hive
	# $(MAKE) -C metaRepo
	# $(MAKE) -C polydb
	# $(MAKE) -C spark
	$(MAKE) -C postgres
	$(MAKE) -C mariadb
	$(MAKE) -C presto
	$(MAKE) -C drill
	$(MAKE) -C jupyter

generate-test-data:
	docker run -it --rm -v test-data:/data --env-file data_generator/data_generator.env --name data-generator tpch-generator

run:
	docker-compose -f .\docker-compose.yml up -d

stop:
	docker-compose -f .\docker-compose.yml down

populate:
	for container in $(DRILL) ; do \
		echo $$container; \
		docker exec $$container /bin/sh -c "/create_plugins.sh"; \
    done
	@echo MY_VAR IS $(POSTGRESS)
	for container in $(POSTGRESS) ; do \
		echo $$container; \
        docker exec $$container /bin/sh -c "cd / && /bin/bash ./import_tpch_sf1.sh"; \
    done
	for container in $(MYSQL) ; do \
		echo $$container; \
		docker exec $$container /bin/sh -c "/import/populate.sh"; \
    done
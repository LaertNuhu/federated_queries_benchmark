POSTGRESS := $(shell docker ps --format '{{.Names}}' --filter name=pg)
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
	docker-compose -f .\docker-compose.yml up

populate:
	@echo MY_VAR IS $(POSTGRESS)
	for container in $(POSTGRESS) ; do \
		echo $$container; \
        docker exec $$container /bin/sh -c "cd / && /bin/bash ./import_tpch_sf1.sh"; \
    done
	docker exec drill /bin/sh -c "./create_plugins.sh"
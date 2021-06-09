import re
import json
import time
from pathlib import Path
from configurator import Configurator


class TestDataGenerator:
    def __init__(self, operator) -> None:
        self.executed = False
        self.operator = operator
        self.__check_test_data_volume_existence()

    def __check_test_data_volume_existence(self):
        result = self.operator.execute("volume ls | grep 'test-data'").decode("utf-8")
        self.executed = True if "test-data" in result else False

    def create_test_data(self):
        if not self.executed:
            start = time.time()
            print(
                "Generating test data. Check the logs of tpch-generator"
                " container if you like to see the progress."
            )
            self.operator.execute(
                "run -it --rm -v test-data:/data --env-file docker_images/data_generator/data_generator.env"
                " --name data-generator tpch-generator"
            )
            end = time.time()
            print(f"Data generation is finished. It took: {str(end - start)}s")
            self.executed = True


class DataIntegrator:
    def __init__(self, operator, configurator) -> None:
        self.operator = operator
        self.config = configurator.parsed_config
        self.tables_schema = json.load(Path("./src/table_schema/tables.json").open())
        self.handler = {
            "mysql": self.__handle_mysql,
            "postgress": self.__handle_postgress,
            "mariadb": self.__handle_mariadb,
        }

    def __check_docker_volume_existence(self, system):
        volumes_already_exist = []
        for source in self.config[system]["sources"]:
            result = self.operator.execute(f"volume ls | grep '{system}'").decode(
                "utf-8"
            )
            volumes_already_exist.append(
                True
            ) if system in result else volumes_already_exist.append(False)
        return all(volumes_already_exist)

    def __create_table(self, source_root, sf, table):
        columns = "("
        for key, value in self.tables_schema[table].items():
            columns = columns + f" {key} {value},"
        columns = columns[:-1] + ");"
        return f"CREATE TABLE {source_root}_{sf}_{table} {columns}"

    def __handle_mysql(self, key, system, source_root, tables):
        # setting up premissions #TODO: username and password are fixed
        grant_privileges = f"echo \"GRANT ALL PRIVILEGES ON *.* TO 'benchmark'@'\%';\" | mysql -u root --password=mysql"
        print(grant_privileges)
        self.operator.execute(f"exec {key} /bin/sh -c '{grant_privileges}'")
        # # print(grant_privileges)
        # # SET GLOBAL local_infile=1;
        # global_local = (
        #     f'echo "SET GLOBAL local_infile=1;" | mysql -u root --password=mysql'
        # )
        # # print(global_local)
        # self.operator.execute(f"exec {key} /bin/sh -c '{global_local}'")
        # # Add public database -> if it exists nobody cares
        # create_database = 'echo "create database public;" | mysql --local-infile=1 -u benchmark --password=secret123'
        # print(create_database)
        # self.operator.execute(f"exec {key} /bin/sh -c '{create_database}'")
        # table creation and import
        # scale_factors = self.config[system]["scale_factors"]
        # for sf in scale_factors:
        #     print("Creating table for ", sf)
        #     for table in tables:
        #         create_table = f'echo "{self.__create_table(source_root, sf, table)}" | mysql public -u benchmark --password=secret123'
        #         print(create_table)
        #         self.operator.execute(f"exec {key} /bin/sh -c '{create_table}'")
        #         import_table = f"echo \"LOAD DATA LOCAL INFILE '/data/{sf}/{table}.tbl' into table {source_root}_{sf}_{table} FIELDS TERMINATED BY '|';\" | mysql public -u benchmark --password=secret123"
        #         # print(import_table)
        #         self.operator.execute(f"exec {key} /bin/sh -c '{import_table}'")

    def __handle_postgress(self, system, tables):
        print("postgress here")
        pass

    def __handle_mariadb(self, system, tables):
        print("mariadb here")
        pass

    def __get_alpha_char(self, string):
        return " ".join(re.findall("[a-zA-Z]+", string))

    def integrate(self, system, resource):
        # print(
        #     f"starting resources for {system}. "
        #     f"Configuration is located on {resource.name}"
        # )
        # if self.__check_docker_volume_existence(system):
        #     self.operator.start_resource(resource)
        # else:
        #     self.operator.start_resource(resource)
        #     print("Waiting until sources are setup.")
        #     time.sleep(15)
        for key, value in self.config[system]["sources"].items():
            # print(f"Creating databases for {system} for source: {key}")
            tables = value["tables"]
            source_root = self.__get_alpha_char(key)
            # self.handler[source_root](system, source_root,tables)
            self.__handle_mysql(key, system, source_root, tables)
            # self.operator.execute(
            #     f"exec {key} /bin/sh -c 'cd / && /bin/bash ./import_tpch_sf1.sh'"
            # )

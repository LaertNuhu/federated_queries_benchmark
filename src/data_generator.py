import re
import json
import time
from pathlib import Path
from configurator import Configurator
from templator import Templator


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
        self.templator = Templator()
        self.handler = {
            "mysql": self.__handle_mysql,
            "postgress": self.__handle_postgress,
            "mariadb": self.__handle_mariadb,
        }

    def __volume_exists(self, source):
        result = self.operator.execute(f"volume ls | grep '{source}'").decode("utf-8")
        return True if source in result else False

    def __handle_mysql(self, system, source):
        template = self.templator.render_mysql_template(self.config[system], source)
        self.operator.execute(f"cp {template} {source}:/{template.name}")
        self.operator.execute(f"exec {source} /bin/bash -c 'chmod +x /{template.name}'")
        self.operator.execute(f"exec {source} /bin/bash -c /{template.name}")

    def __handle_postgress(self, system, source):
        template = self.templator.render_postgres_template(self.config[system], source)
        self.operator.execute(f"cp {template} {source}:/{template.name}")
        self.operator.execute(f"exec {source} /bin/bash -c 'chmod +x /{template.name}'")
        self.operator.execute(f"exec {source} /bin/bash -c /{template.name}")

    def __handle_mariadb(self, system, source):
        print("mariadb here")
        pass

    def __get_alpha_char(self, string):
        return " ".join(re.findall("[a-zA-Z]+", string))

    def integrate(self, system, resource):
        unconfigured_sources = [
            source
            for source in self.config[system]["sources"]
            if not self.__volume_exists(source)
        ]
        self.operator.start_resource(resource)
        if unconfigured_sources:
            print("Waiting until sources are setup.")
            time.sleep(30)
        for source in unconfigured_sources:
            print(f"Creating databases for {system} for source: {source}")
            source_root = self.__get_alpha_char(source)
            self.handler[source_root](system, source)

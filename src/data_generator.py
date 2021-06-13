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

    def __handle_mysql(self, system, source):
        template = self.templator.render_mysql_template(self.config[system], source)
        self.operator.execute(f"cp {template} {source}:/{template.name}")
        self.operator.execute(f"exec {source} /bin/bash -c 'chmod +x {template.name}'")

    def __handle_postgress(self, system, source):
        print("Not there yet")
        pass

    def __handle_mariadb(self, system, source):
        print("mariadb here")
        pass

    def __get_alpha_char(self, string):
        return " ".join(re.findall("[a-zA-Z]+", string))

    def integrate(self, system, resource):
        print(
            f"starting resources for {system}. "
            f"Configuration is located on {resource.name}"
        )
        if self.__check_docker_volume_existence(system):
            self.operator.start_resource(resource)
        else:
            self.operator.start_resource(resource)
            print("Waiting until sources are setup.")
            time.sleep(15)
        for source in self.config[system]["sources"]:
            print(f"Creating databases for {system} for source: {source}")
            source_root = self.__get_alpha_char(source)
            self.handler[source_root](system, source)

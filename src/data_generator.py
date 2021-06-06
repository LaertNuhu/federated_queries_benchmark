import time
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

    def __handle_mysql():
        pass

    def __handle_posgress():
        pass

    def __handle_mariadb():
        pass

    def integrate(self, system):
        print("Waiting until sources are setup.")
        time.sleep(10)
        for source in self.config[system]["sources"]:
            print(f"Creating databases for {system} for source: {source}")
            self.operator.execute(
                f"exec {source} /bin/sh -c 'cd / && /bin/bash ./import_tpch_sf1.sh'"
            )

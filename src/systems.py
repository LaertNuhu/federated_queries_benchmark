import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
import prestodb.dbapi as presto
from pydrill.client import PyDrill
from templator import Templator
from configurator import Configurator
from docker_operator import Operator


class System(ABC):
    @abstractmethod
    def setup(self):
        raise NotImplementedError("subclasses must override setup()!")

    @abstractmethod
    def run_query(self, sql, show):
        raise NotImplementedError("subclasses must override run_query()!")

    @abstractmethod
    def post_startup(self):
        raise NotImplementedError("subclasses must override post_startup()!")


class Presto(System):
    def __init__(self, host="localhost", port=8080, user="demo"):
        self.configurator = Configurator(system="Presto")
        self.templator = Templator()
        self.operator = Operator()
        conn = presto.Connection(host=host, port=port, user=user)
        self.cur = conn.cursor()

    def setup(self):
        self.__create_catalog()
        self.__create_docker_image()
        self.__update_image()
        self.__cleanup()

    def run_query(self, sql, show=False):
        start = time.time()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        end = time.time()
        if show:
            return result
        return str(end-start)

    def post_startup(self):
        pass

    def __create_catalog(self):
        sources = self.configurator.get_config()["sources"]
        self.templator.render_catalog_template(sources)

    def __update_image(self):
        self.operator.run("docker build -t presto .")

    def __create_docker_image(self):
        dockerfile = Path("Dockerfile")
        dockerfile.write_text(
            """
            FROM fedbench/presto
            ADD catalog etc/catalog
            """
        )

    @staticmethod
    def __cleanup():
        Path("Dockerfile").unlink()
        [path.unlink() for path in Path("catalog").iterdir()]
        Path("catalog").rmdir()


class Drill(System, PyDrill):
    def __init__(self, host="localhost", port=8080):
        self.configurator = Configurator(system="Drill")
        self.operator = Operator()
        PyDrill.__init__(self, host=host, port=port)

    def setup(self):
        self.__create_configs()
        self.__create_docker_image()
        self.__update_image()
        self.__cleanup()

    def run_query(self, sql, timeout=100000, show=False):
        start = time.time()
        if show:
            return self.query(sql, timeout=timeout).to_dataframe()
        self.query(sql, timeout=timeout)
        end = time.time()
        return str(end-start)

    def post_startup(self):
        time.sleep(20)
        print("Drill needs some time until is fully started.")
        self.__enable_storages()
        self.run_query("ALTER SYSTEM SET `planner.memory.percent_per_query` = 1.0")

    def __config_template(self, name, **kwargs):
        if "postgres" in name:
            driver = "org.postgresql.Driver"
        if "mysql" in name:
            driver = "com.mysql.jdbc.Driver"
        return {
            "name": name,
            "config": {
                "type": "jdbc",
                "enabled": True,
                "driver": driver,
                "url": kwargs["url"],
                "username": kwargs["user"],
                "password": kwargs["password"],
            },
        }

    def __enable_storages(self):
        self.operator.run('docker exec drill /bin/sh -c "/create_plugins.sh";')

    def __update_image(self):
        self.operator.run("docker build -t drill .")

    def __create_docker_image(self):
        dockerfile = Path("Dockerfile")
        dockerfile.write_text(
            """
            FROM fedbench/drill
            COPY configs /configs
            """
        )

    def __create_configs(self):
        sources = self.configurator.get_config()["sources"]
        for source in sources:
            config = self.__config_template(source, **sources[source])
            Path(f"./configs/{source}.json").parent.mkdir(parents=True, exist_ok=True)
            with Path(f"./configs/{source}.json").open("w") as outfile:
                json.dump(config, outfile)

    @staticmethod
    def __cleanup():
        Path("Dockerfile").unlink()
        [path.unlink() for path in Path("./configs").iterdir()]
        Path("./configs").rmdir()


class Spark(System):
    def __init__(self) -> None:
        self.configurator = Configurator(system="Spark")
        self.templator = Templator()
        self.operator = Operator()

    def setup(self):
        Path(f"./src/compose_files/app.py").write_text("")

    def run_query(self, sql):
        self.__create_configs(sql)
        start = time.time()
        self.operator.run(
            f'docker exec client /bin/sh -c "python /app.py"'
        )
        end = time.time()
        return str(end-start)

    def post_startup(self):
        pass

    def __create_configs(self,sql):
        self.templator.render_spark_app_template(self.configurator.get_config(),sql)


class Hive(System):
    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        pass

    def run_query(self, sql, show):
        raise Exception("System is not implemented yet")
        pass

    def post_startup(self):
        pass

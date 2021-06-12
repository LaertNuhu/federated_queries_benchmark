from abc import ABC, abstractmethod
from os import PathLike, unlink
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
        self.cur.execute(sql)
        result = self.cur.fetchall()
        if show:
            return result

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
    def __init__(self, host="localhost", port=8047):
        PyDrill.__init__(self, host=host, port=8047)

    def setup(self):
        pass

    def run_query(self, sql, timeout=100000, show=False):
        if show:
            return self.query(sql, timeout=timeout).to_dataframe()
        return self.query(sql, timeout=timeout)


class Spark(System):
    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        pass

    def run_query(self, sql, show):
        pass


class Hive(System):
    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        pass

    def run_query(self, sql, show):
        pass


if __name__ == "__main__":
    presto = Presto()
    presto.run_query("Show catalogs", show=True)

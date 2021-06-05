from abc import ABC, abstractmethod
import prestodb.dbapi as presto
from pydrill.client import PyDrill


class System(ABC):
    @abstractmethod
    def run_query(self, sql, show):
        raise NotImplementedError("subclasses must override run_query()!")


class Presto(System):
    def __init__(self, host="presto", port=8080, user="demo"):
        self.conn = presto.Connection(host="presto", port=8080, user="demo")
        self.cur = self.conn.cursor()

    def run_query(self, sql, show=False):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        if show:
            return result

    def create_catalog(self):
        pass


class Drill(System, PyDrill):
    def __init__(self, host="drill", port=8047):
        PyDrill.__init__(self, host="drill", port=8047)

    def run_query(self, sql, timeout=100000, show=False):
        if show:
            return self.query(sql, timeout=timeout).to_dataframe()
        return self.query(sql, timeout=timeout)


class Spark(System):
    def __init__(self) -> None:
        super().__init__()

    def run_query(self, sql, show):
        pass


class Hive(System):
    def __init__(self) -> None:
        super().__init__()

    def run_query(self, sql, show):
        pass

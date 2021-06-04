import re
import prestodb.dbapi as presto
from pydrill.client import PyDrill
import pandas as pd
from configurator import Configurator


class Benchmarker:
    def __init__(self, system="all"):
        self.configurator = Configurator(system=system)
        self.queries = self.configurator.get_queries()

    def sort_human(l):
        convert = lambda text: float(text) if text.isdigit() else text
        alphanum = lambda key: [
            convert(c) for c in re.split("([-+]?[0-9]*\.?[0-9]*)", key)
        ]
        l.sort(key=alphanum)
        return l

    def benchmark(self, system, query, iterations=1):
        sum = 0
        count = 0
        for _ in range(iterations):
            count = count + 1
            start = time.time()
            system.run_query(query)
            end = time.time()
            sum = sum + (end - start)
        return sum / count

    def run_and_save_results(self, system, queries, iterations=1):
        f = Path(f"{type(system).__name__}.csv").open("a")
        log = Path("errors.log").open("a")
        for query in queries[:-1]:
            try:
                benchmark_result = benchmark(
                    system, query_dict[query], iterations=iterations
                )
                f.write(str(benchmark_result))
                time.sleep(10)
            except Exception as e:
                f.write("0")
                log.write(str(e))
            f.write(",")
            f.flush()
        try:
            benchmark_result = benchmark(
                system, query_dict[queries[-1]], iterations=iterations
            )
            f.write(str(benchmark_result))
        except Exception as e:
            f.write("0")
            log.write(str(e))
        f.write("\n")
        log.write("\n")
        log.close()
        f.close()


if __name__ == "__main__":
    import json

    benchmarker = Benchmarker()
    queries = benchmarker.queries
    with open("data.json", "w") as outfile:
        json.dump(queries, outfile)

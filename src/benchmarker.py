import re
import sys
import time
import pandas as pd
from configurator import Configurator
from docker_operator import DockerOperator
from pathlib import Path
import random


class Benchmarker:
    def __init__(self, system="all"):
        self.configurator = Configurator(system=system)
        self.queries = self.configurator.get_queries()
        self.operator = DockerOperator()

    def __sort_human(self, l):
        """Sorts a list of strings correctly."""
        convert = lambda text: float(text) if text.isdigit() else text
        alphanum = lambda key: [
            convert(c) for c in re.split("([-+]?[0-9]*\.?[0-9]*)", key)
        ]
        l.sort(key=alphanum)
        return l

    def benchmark(self, system, query):
        """Runs query based on a system"""
        try:
            start = time.time()
            # system.run_query(query)
            time.sleep(random.random() * 2)
            end = time.time()
            return str(end - start)
        except Exception as e:
            log = Path("./benchmark/error/errors.log").open("a")
            log.write(str(e))
            log.write("\n")
            return "0"

    def __create_results_file(self, system):
        """Creates results csv file"""
        return Path(f"./benchmark/results/{system}.csv").open("a")

    def __iterate_systems(self, callback):
        """Execute a callback function for every system."""
        systems = list(self.queries.keys())
        resources = self.configurator.get_rendered_sources()
        zip_list = list(zip(systems, resources))
        for system, resource in zip_list:
            # start resources
            print(
                f"starting resources for {system}. Configuration is on {resource.name}"
            )
            self.operator.start_resource(resource)
            # do smth with the resources
            callback(system)
            # stop resources
            print(f"deleting resources for {system}")
            self.operator.stop_resource(resource)

    def __iterate_scale_factors(self, system, callback):
        """Execute a callback function for every scale factor"""
        scale_factors = list(self.queries[system].keys())
        for scale_factor in scale_factors:
            callback(scale_factor)

    def __construct_header(self, system):
        """It creates the header string and adds into each result file."""
        first_scale_factor = list(self.queries[system].keys())[0]
        file = self.__create_results_file(system)
        queries_initials = [
            key for key in self.queries[system][first_scale_factor].keys()
        ]
        reordered_query_initials = self.__sort_human(queries_initials)
        queries_initials_to_string = ",".join(reordered_query_initials)
        header = f"sf,{queries_initials_to_string}"
        file.write(header)
        file.write("\n")
        file.close()

    def write_headers(self):
        """Executes public function."""
        self.__iterate_systems(lambda system: self.__construct_header(system))

    def __run_query_and_save_results(self, system, scaleFactor, iterations=1):
        f = self.__create_results_file(system)
        queries = self.queries[system][scaleFactor]
        queries_ids = [key for key in queries.keys()]
        reordered_queries_ids = self.__sort_human(queries_ids)
        for _ in range(iterations + 1):
            f.write(scaleFactor)
            f.flush()
            for query_id in reordered_queries_ids:
                benchmark_result = self.benchmark(system, queries[query_id])
                f.write(",")
                f.write(benchmark_result)
                f.flush()
            f.write("\n")

    def run_benchmarks(self):
        self.__iterate_systems(
            lambda system: benchmarker.__iterate_scale_factors(
                system, lambda sf: self.__run_query_and_save_results(system, sf)
            )
        )


if __name__ == "__main__":
    benchmarker = Benchmarker()
    benchmarker.run_benchmarks()

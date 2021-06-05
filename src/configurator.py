from typing import List
import yaml
import pandas as pd
from pathlib import Path
from templator import Templator
from mapper import Mapper
import re


class Configurator:
    def __init__(self, system="all"):
        self.parsed_config = self.parse_config()
        self.mapper = Mapper()
        self.system = system.lower()

    def parse_config(self):
        config = Path("./config.yml").read_text()
        parsed_configs = yaml.load(config, Loader=yaml.FullLoader)
        return parsed_configs

    def build_source_dict(self):
        """Creates a dict with tables where they are located"""
        result = {}
        system = self.get_config()
        for source, config in system["sources"].items():
            [result.update({table: source}) for table in config["tables"]]
        return result

    def get_config(self):
        system_name = self.system.lower()
        if system_name in self.parsed_config.keys():
            return self.parsed_config[system_name]
        raise ValueError(
            f"{system_name} is not configured. Add the configurations in config.yml"
        )

    def get_scales(self):
        return self.get_config()["scale_factors"]

    def create_range(self, queries):
        """It takes the lazy form of queries range and turns it into a list of queries"""
        results = []
        for query in queries:
            numbers = re.findall("[0-9]+", query)
            letters = list(set(re.findall("[a-zA-Z]", query)))
            if len(letters) == 1:
                for count in range(int(numbers[0]), int(numbers[-1]) + 1):
                    results.append(f"{letters[0]}{count}")
        return results

    def get_benchmark_queries(self):
        system = self.get_config()
        queries_keys = system["queries"]
        long = [key for key in queries_keys if ":" not in key]
        layzy = [key for key in queries_keys if ":" in key]
        long_form = self.create_range(layzy)
        long.extend(long_form)
        return long

    def render_queries(self, scale, sources):
        to_benchmark = self.get_benchmark_queries()
        templator = Templator(queries_path="./benchmark/queries", selected=to_benchmark)
        sources_config = self.mapper.map_tables_to_sources(scale=scale, **sources)
        return templator.render_queries(sources_config)

    def get_queries(self):
        result = {}
        if self.system == "all":
            for system in self.parsed_config:
                self.system = system.lower()
                result[self.system] = {}
                sources = self.build_source_dict()
                scales = self.get_scales()
                if isinstance(scales, List):
                    for scale in scales:
                        rendered_queries = self.render_queries(scale, sources)
                        result[self.system][scale] = rendered_queries
                else:
                    rendered_queries = self.render_queries(scales, sources)
                    result[self.system][scales] = rendered_queries
        else:
            sources = self.build_source_dict()
            scales = self.get_scales()
            result[self.system] = {}
            if isinstance(scales, List):
                for scale in scales:
                    rendered_queries = self.render_queries(scale, sources)
                    result[self.system][scale] = rendered_queries
            else:
                rendered_queries = self.render_queries(scales, sources)
                result[self.system][scales] = rendered_queries
        return result

    def get_rendered_sources(self):
        templator = Templator()
        if self.system == "all":
            templator.render_sources_template(config=self.parsed_config)
        else:
            templator.render_sources_template(
                system=self.system, config=self.get_config()
            )


if __name__ == "__main__":
    config = Configurator()
    config.get_rendered_sources()

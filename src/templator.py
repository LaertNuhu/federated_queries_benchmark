import jinja2
from pathlib import Path
import json


class Templator:
    def __init__(self, queries_path=None, selected=None) -> None:
        self.queries_path = queries_path
        self.selected = selected
        self.tables_schema = json.load(Path("./src/table_schema/tables.json").open())

    def render_queries(self, sources):
        """Returns a dict where the key is the tpch query name and the value is the rendered query"""
        result = {}
        querie_paths = [q for q in Path(self.queries_path).iterdir()]
        for path in querie_paths:
            key = path.name.split(".")[0]
            value = jinja2.Template(path.read_text()).render(**sources)
            result.update({key: value}) if key in self.selected else None
        return result

    def render_sources_template(self, config, system=None):
        sources_config_yml = Path("./src/templates/docker-compose-sources.yml.j2")
        results = []
        if "sources" in config:
            result = jinja2.Template(sources_config_yml.read_text()).render(
                system=system, **config
            )
            Path(f"./src/compose_files/docker-compose-{system}.yml").parent.mkdir(
                parents=True, exist_ok=True
            )
            Path(f"./src/compose_files/docker-compose-{system}.yml").write_text(result)
            results.append(Path(f"./src/compose_files/docker-compose-{system}.yml"))
        else:
            for system in config:
                result = jinja2.Template(sources_config_yml.read_text()).render(
                    system=system, **config[system]
                )
                Path(f"./src/compose_files/docker-compose-{system}.yml").parent.mkdir(
                    parents=True, exist_ok=True
                )
                Path(f"./src/compose_files/docker-compose-{system}.yml").write_text(
                    result
                )
                results.append(Path(f"./src/compose_files/docker-compose-{system}.yml"))
        return results

    def __create_columns(self, table):
        columns = "("
        for key, value in self.tables_schema[table].items():
            columns = columns + f" {key} {value},"
        columns = columns[:-1] + ");"
        return columns

    def render_mysql_template(self, config, key):
        sources_config_yml = Path("./src/templates/mysql_setup.sh.j2")
        scale_factors = config["scale_factors"]
        if "mysql" not in key:
            return None

        tables = dict.fromkeys(config["sources"][key]["tables"])
        columns = {column: self.__create_columns(column) for column in tables}
        result = jinja2.Template(sources_config_yml.read_text()).render(
            **config["sources"][key], scale_factors=scale_factors, columns=columns
        )
        Path(f"./src/compose_files/{key}.sh").write_text(result)
        return Path(f"./src/compose_files/{key}.sh")

    def render_postgres_template(self, config, key):
        sources_config_yml = Path("./src/templates/postgres_setup.sh.j2")
        scale_factors = config["scale_factors"]
        if "postgres" not in key:
            return None

        tables = dict.fromkeys(config["sources"][key]["tables"])
        columns = {column: self.__create_columns(column) for column in tables}
        result = jinja2.Template(sources_config_yml.read_text()).render(
            **config["sources"][key], scale_factors=scale_factors, columns=columns
        )
        Path(f"./src/compose_files/{key}.sh").write_text(result)
        return Path(f"./src/compose_files/{key}.sh")

    def render_catalog_template(self, sources):
        """Creates catalogs for mysql and posgres"""
        sources_config_yml = Path("./src/templates/catalog.properties.j2")
        for source in sources:
            result = jinja2.Template(sources_config_yml.read_text()).render(
                **sources[source], key=source
            )
            Path(f"./catalog/{source}.properties").parent.mkdir(
                parents=True, exist_ok=True
            )
            Path(f"./catalog/{source}.properties").write_text(result)

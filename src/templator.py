import jinja2
import yaml
from pathlib import Path


class Templator:
    def __init__(self, queries_path=None, selected=None) -> None:
        self.queries_path = queries_path
        self.selected = selected

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

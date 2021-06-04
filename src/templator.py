import jinja2
from pathlib import Path


class Templator:
    def __init__(self, queries_path, selected) -> None:
        self.queries_path = queries_path
        self.selected = selected

    def get_rendered_queries(self, sources):
        """Returns a dict where the key is the tpch query name and the value is the rendered query"""
        result = {}
        querie_paths = [q for q in Path(self.queries_path).iterdir()]
        for path in querie_paths:
            key = path.name.split(".")[0]
            value = jinja2.Template(path.read_text()).render(**sources)
            result.update({key: value}) if key in self.selected else None
        return result

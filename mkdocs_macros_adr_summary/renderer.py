from pathlib import Path
from typing import Iterable, Optional

from jinja2 import Environment, FileSystemLoader

from .interfaces import ADRDocument


class Jinja2Renderer:
    @staticmethod
    def summary(
        documents: Iterable[ADRDocument],
        mkdocs_base_path: Path,
        template_file: Optional[str] = None,
    ) -> str:
        if template_file:
            template_env = Environment(
                loader=FileSystemLoader(searchpath=mkdocs_base_path),
                autoescape=True,
            )
            template = template_env.get_template(template_file)
        else:
            template_env = Environment(
                loader=FileSystemLoader(searchpath=Path(__file__).parent),
                autoescape=True,
            )
            template = template_env.get_template("template.jinja")

        return template.render(documents=documents)

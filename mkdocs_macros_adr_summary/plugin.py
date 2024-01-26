import os
import re
from pathlib import Path
from typing import Optional

from mkdocs_macros.plugin import MacrosPlugin

from .factory import get_parser
from .interfaces import TYPE_ADRStyle
from .renderer import Jinja2Renderer

ADR_REGEX = re.compile("^[0-9]{4}-[\\w-]+\\.md*")


def adr_summary(
    env: MacrosPlugin,
    adr_path: str,
    adr_style: TYPE_ADRStyle,
    template_file: Optional[str] = None,
) -> str:
    absolute_path = Path(env.project_dir).joinpath(adr_path)
    parser = get_parser(adr_style)

    documents = [
        parser.parse(absolute_path.joinpath(f), env.conf["docs_dir"])
        for f in os.listdir(absolute_path)
        if os.path.isfile(absolute_path.joinpath(f)) and ADR_REGEX.match(f)
    ]

    return Jinja2Renderer.summary(
        documents=documents,
        mkdocs_base_path=Path(env.project_dir),
        template_file=template_file,
    )

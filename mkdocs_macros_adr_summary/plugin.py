import os
import re
from pathlib import Path
from typing import Optional

from mkdocs_macros.plugin import MacrosPlugin

from .factory import get_parser
from .interfaces import ADRStyle
from .renderer import Jinja2Renderer

ADR_REGEX = re.compile("^[0-9]{4}-[\\w-]+\\.md*")


def adr_summary(
    env: MacrosPlugin,
    adr_path: str,
    adr_style: ADRStyle = "nygard",
    template_path: Optional[str] = None,
) -> str:
    mkdocs_base_path = Path(env.config.config_file_path).parent
    absolute_path = mkdocs_base_path.joinpath(adr_path)
    parser = get_parser(adr_style)

    documents = [
        parser.parse(absolute_path.joinpath(f))
        for f in os.listdir(absolute_path)
        if os.path.isfile(absolute_path.joinpath(f)) and ADR_REGEX.match(f)
    ]

    return Jinja2Renderer.summary(
        documents=documents,
        mkdocs_base_path=mkdocs_base_path,
        template_path=template_path,
    )

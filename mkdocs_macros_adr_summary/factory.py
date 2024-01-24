from typing import Dict, Type

from .interfaces import ADRParser, ADRStyle
from .parser import NygardParser

parser_registry: Dict[ADRStyle, Type[ADRParser]] = {"nygard": NygardParser}


def get_parser(adr_style: ADRStyle) -> Type[ADRParser]:
    try:
        parser = parser_registry[adr_style]
    except KeyError:
        raise ValueError(f"Format {adr_style} not supported")

    return parser

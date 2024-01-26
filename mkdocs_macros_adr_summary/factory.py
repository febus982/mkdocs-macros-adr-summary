from typing import Dict, Type

from .interfaces import ADRParser, TYPE_ADRStyle
from .parser import MADR3Parser, NygardParser

parser_registry: Dict[TYPE_ADRStyle, Type[ADRParser]] = {
    "nygard": NygardParser,
    "MADR3": MADR3Parser,
}


def get_parser(adr_style: TYPE_ADRStyle) -> Type[ADRParser]:
    try:
        parser = parser_registry[adr_style]
    except KeyError:
        raise ValueError(f"Format {adr_style} not supported")

    return parser

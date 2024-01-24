from unittest.mock import patch

import pytest

from mkdocs_macros_adr_summary.factory import get_parser, parser_registry


def test_parser_factory():
    with patch.dict(parser_registry, {"some_format": "some_value"}, clear=True):
        assert get_parser("some_format") == "some_value"

        with pytest.raises(Exception):
            get_parser("inexisting")

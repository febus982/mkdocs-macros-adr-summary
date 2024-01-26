from datetime import datetime
from pathlib import Path

import pytest

from mkdocs_macros_adr_summary.parser.exceptions import InvalidFileError
from mkdocs_macros_adr_summary.parser.madr3 import MADR3Parser


@pytest.mark.parametrize(
    ["filename", "expected_metadata"],
    [
        (
            "valid_with_metadata.md",
            {
                "status": "Accepted",
                "statuses": tuple(["Accepted"]),
                "date": datetime.fromisoformat("2024-01-20").date(),
                "deciders": "Nick Fury",
                "consulted": "Anthony Stark",
                "informed": "Thor Odinson",
            },
        ),
        (
            "valid_without_metadata.md",
            {
                "status": None,
                "statuses": tuple(),
                "date": None,
                "deciders": None,
                "consulted": None,
                "informed": None,
            },
        ),
    ],
)
def test_parse_valid_document(
    filename: str, expected_metadata: dict, adr_document_factory
):
    assert MADR3Parser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/madr3/{filename}"),
        base_path=Path(__file__).parent,
    ) == adr_document_factory(
        file_path=f"../adr_docs/madr3/{filename}",
        title="Use Markdown Any Decision Records",
        **expected_metadata,
    )


def test_parse_invalid_blank_document():
    with pytest.raises(InvalidFileError):
        MADR3Parser.parse(
            Path(__file__).parent.joinpath("adr_docs/madr3/invalid_blank_document.md"),
            base_path=Path(__file__).parent,
        )


@pytest.mark.parametrize(
    ["filename"],
    [("invalid_title_h3.md",), ("invalid_title_p.md",)],
)
def test_parse_invalid_title(filename: str, adr_document_factory):
    document = MADR3Parser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/madr3/{filename}"),
        base_path=Path(__file__).parent,
    )
    assert document.title == adr_document_factory().title


def test_parse_invalid_headers():
    with pytest.raises(InvalidFileError):
        MADR3Parser.parse(
            Path(__file__).parent.joinpath("adr_docs/madr3/invalid_headers.md"),
            base_path=Path(__file__).parent,
        )

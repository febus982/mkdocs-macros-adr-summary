from datetime import datetime
from pathlib import Path

import pytest

from mkdocs_macros_adr_summary.parser.exceptions import InvalidFileError
from mkdocs_macros_adr_summary.parser.madr2 import MADR2Parser


@pytest.mark.parametrize(
    ["filename", "expected_metadata"],
    [
        (
            "valid_with_metadata.md",
            {
                "status": "Accepted",
                "statuses": tuple(["Accepted"]),
                "date": datetime.fromisoformat("2024-01-24").date(),
                "deciders": "Nick Fury",
                "consulted": None,
                "informed": None,
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
    assert MADR2Parser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/madr2/{filename}"),
        base_path=Path(__file__).parent,
    ) == adr_document_factory(
        file_path=f"../adr_docs/madr2/{filename}",
        title="Use Markdown Any Decision Records",
        **expected_metadata,
    )


def test_parse_invalid_blank_document():
    with pytest.raises(InvalidFileError):
        MADR2Parser.parse(
            Path(__file__).parent.joinpath("adr_docs/madr2/invalid_blank_document.md"),
            base_path=Path(__file__).parent,
        )


@pytest.mark.parametrize(
    ["filename"],
    [("invalid_title_h3.md",), ("invalid_title_p.md",)],
)
def test_parse_invalid_title(filename: str, adr_document_factory):
    document = MADR2Parser.parse(
        Path(__file__).parent.joinpath(f"adr_docs/madr2/{filename}"),
        base_path=Path(__file__).parent,
    )
    assert document.title == adr_document_factory().title


def test_invalid_headers_are_ignored():
    document = MADR2Parser.parse(
        Path(__file__).parent.joinpath("adr_docs/madr2/invalid_headers.md"),
        base_path=Path(__file__).parent,
    )
    assert document.status == "Accepted"
    assert document.statuses == tuple(["Accepted"])
    assert document.date == datetime.fromisoformat("2024-01-24").date()
    assert document.deciders == "Nick Fury"

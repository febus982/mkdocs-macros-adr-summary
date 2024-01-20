from pathlib import Path

from mkdocs_macros_adr_summary.interfaces import ADRDocument, ADRParser


class ADRNygardParser(ADRParser):
    @staticmethod
    def parse(file_path: Path) -> ADRDocument:
        return ADRDocument(filename=str(file_path))

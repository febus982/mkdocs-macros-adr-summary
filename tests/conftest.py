import factory
from pytest_factoryboy import register

from mkdocs_macros_adr_summary.interfaces import ADRDocument


# This generates `adr_document_factory` and `adr_document` fixtures
@register
class ADRDocumentFactory(factory.Factory):
    class Meta:
        model = ADRDocument

    file_path: str = "../adr_docs/madr3/some-architectural-decision.md"

import hashlib
import json
from pathlib import Path

from pydantic import TypeAdapter
from opspilot.knowledge.models import PolicyMetadata, PolicyDocument

class PolicyDocumentLoader:
    def __init__(self, directory: Path) -> None:
        self._directory = directory.resolve()

    def load(self) -> list[PolicyDocument]:
        manifest_path = self._directory / "manifest.json"

        raw_metadata = json.loads(manifest_path.read_text(encoding="utf-8"))

        metadata_list = TypeAdapter(list[PolicyMetadata]).validate_python(raw_metadata)

        documents: list[PolicyDocument] = []

        seen_versions: set[tuple[str,str]] = set()

        for metadata in metadata_list:
            document_key = metadata.document_id, metadata.version

            if document_key in seen_versions:
                raise ValueError(f"Duplicate document version found: {document_key}")

            seen_versions.add(document_key)
            document = self._load_document(metadata)
            documents.append(document)

        return documents

    def _load_document(self, metadata: PolicyMetadata) -> PolicyDocument:
        document_path = (self._directory / metadata.source_path).resolve()

        if not document_path.is_relative_to(self._directory):
            raise ValueError(f"Document path is outside the knowledge directory")
        
        content = document_path.read_text(encoding="utf-8")

        if not content.strip():
            raise ValueError(f"Document empty: {metadata.source_path}")

        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        return PolicyDocument(metadata=metadata, content=content, content_hash=content_hash)
import json
from pathlib import Path

import pytest

from opspilot.knowledge.loader import PolicyDocumentLoader

from pydantic import ValidationError


def create_test_policy(directory: Path, content: str = "Test refund policy.") -> None:
    manifest = [
        {
            "document_id": "POL-001",
            "title": "Refund Policy",
            "version": "1.0",
            "category": "refund",
            "effective_from": "2026-01-01",
            "status": "active",
            "source_path": "refund_policy.md",
        }
    ]

    manifest_path = directory / "manifest.json"

    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    document_path = directory / "refund_policy.md"
    document_path.write_text(content, encoding="utf-8")

def test_load_policy_document(tmp_path: Path) -> None:

    create_test_policy(tmp_path)

    loader = PolicyDocumentLoader(directory=tmp_path)

    documents = loader.load()

    assert len(documents) == 1

    document = documents[0]

    assert document.metadata.document_id == "POL-001"

    assert document.metadata.version == "1.0"

    assert document.content == "Test refund policy."

    assert len(document.content_hash) == 64


def test_content_hash_is_consistent(tmp_path: Path) -> None:

    create_test_policy(tmp_path)

    loader = PolicyDocumentLoader(directory=tmp_path)

    first_document = loader.load()[0]
    second_document = loader.load()[0]

    assert first_document.content_hash == second_document.content_hash


def test_content_hash_changes(tmp_path: Path) -> None:

    create_test_policy(tmp_path, content="Return window is 30 days.")

    loader = PolicyDocumentLoader(directory=tmp_path)

    original = loader.load()[0]

    document_path = tmp_path / "refund_policy.md"

    document_path.write_text("Return window is 45 days.", encoding="utf-8")

    updated = loader.load()[0]

    assert original.content_hash != updated.content_hash


def test_rejects_empty_document(tmp_path: Path) -> None:

    create_test_policy(tmp_path, content="")

    loader = PolicyDocumentLoader(directory=tmp_path)

    with pytest.raises(ValueError, match="Document empty"):
        loader.load()

def test_rejects_missing_document(tmp_path: Path) -> None:

    create_test_policy(tmp_path)

    document_path = tmp_path / "refund_policy.md"

    document_path.unlink()

    loader = PolicyDocumentLoader(directory=tmp_path)

    with pytest.raises(FileNotFoundError):
        loader.load()

def test_rejects_invalid_document_status(tmp_path: Path) -> None:

    create_test_policy(tmp_path)

    manifest_path = tmp_path / "manifest.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    manifest[0]["status"] = "unknown"

    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    loader = PolicyDocumentLoader(directory=tmp_path)

    with pytest.raises(ValidationError):
        loader.load()


def test_rejects_duplicate_document_version(tmp_path: Path) -> None:

    create_test_policy(tmp_path)

    manifest_path = tmp_path / "manifest.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    manifest.append(manifest[0].copy())

    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    loader = PolicyDocumentLoader(directory=tmp_path)

    with pytest.raises(ValueError, match="Duplicate document version"):
        loader.load()


def test_rejects_path_outside_directory(tmp_path: Path) -> None:

    create_test_policy(tmp_path)

    manifest_path = tmp_path / "manifest.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    manifest[0]["source_path"] = "../outside.md"

    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    loader = PolicyDocumentLoader(directory=tmp_path)

    with pytest.raises(ValueError, match="outside the knowledge directory"):
        loader.load()
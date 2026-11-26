from pathlib import Path

from opspilot.knowledge.loader import PolicyDocumentLoader

def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    policy_directory = project_root / "knowledge" / "policies"

    loader = PolicyDocumentLoader(policy_directory)
    documents = loader.load()

    print(f"\nLoaded {len(documents)} policy documents")

    for document in documents:
        print("-"*60)
        print(f"Document ID: {document.metadata.document_id}")
        print(f"Title: {document.metadata.title}")
        print(f"Version: {document.metadata.version}")
        print(f"Category: {document.metadata.category}")
        print(f"Effective From: {document.metadata.effective_from}")
        print(f"Status: {document.metadata.status}")
        print(f"Source Path: {document.metadata.source_path}")
        print(f"Content Hash: {document.content_hash}")
        print("-"*60)

if __name__ == "__main__":
    main()

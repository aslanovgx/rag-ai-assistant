# src/loader.py
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from backend.src.text_cleaner import clean_text


def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    return loader.load()


def load_docx(file_path: str):
    loader = Docx2txtLoader(file_path)
    return loader.load()


def process_documents(documents, file_path: str):
    """
    Apply cleaning and metadata enrichment to documents.
    """

    processed_docs = []

    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

        if not doc.metadata:
            doc.metadata = {}

        doc.metadata["source"] = file_path
        doc.metadata["page"] = doc.metadata.get("page", None)

        processed_docs.append(doc)

    return processed_docs


def load_document(file_path: str):
    """
    Unified document loader (PDF + DOCX)
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        raw_docs = load_pdf(file_path)

    elif extension == ".docx":
        raw_docs = load_docx(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")

    return process_documents(raw_docs, file_path)


# Now:
# - Each loader handles only its file type
# - A shared processing function applies cleaning and metadata

# This made the ingestion pipeline more modular, reusable, and easier to extend.
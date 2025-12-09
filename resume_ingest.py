# resume_ingest.py

from resume_utils import extract_text_from_pdf_bytes
from vector_store import vector_store


def ingest_resume_into_vector_db(pdf_bytes: bytes, metadata: dict):
    """
    Extracts text from resume PDF, embeds it, stores in Qdrant with metadata.
    """

    try:
        text = extract_text_from_pdf_bytes(pdf_bytes)

        if not text.strip():
            print("WARNING: Resume text extraction returned empty. Skipping ingestion.")
            return False

        vs = vector_store()

        # LangChain takes care of generating embeddings
        vs.add_texts(
            texts=[text],
            metadatas=[metadata]
        )

        print(f"Resume stored in Qdrant → {metadata.get('filename')}")
        return True

    except Exception as e:
        print(f"ERROR during Qdrant ingestion: {e}")
        return False

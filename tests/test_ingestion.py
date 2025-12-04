import os
import sys
import pytest
from uuid import uuid4

# ---------------------------------------------------------
# Ensure tests can import project modules
# ---------------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from vector_store import vector_store, qdrant_client, COLLECTION_NAME
from resume_utils import extract_text_from_pdf_bytes
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv
load_dotenv()


TEST_RESUME_DIR = os.path.join(PROJECT_ROOT, "test_resumes")


def test_ingest_resumes():
    """
    Verify that resumes in test_resumes/ can be:
    - read
    - converted to text
    - embedded
    - stored into Qdrant
    """
    # Vector store and raw client
    vs = vector_store()
    client = qdrant_client()

    # --------------------------------------------------
    # Cleanup existing collection (if any)
    # --------------------------------------------------
    try:
        client.delete_collection(collection_name=COLLECTION_NAME)
    except Exception:
        pass

    # --------------------------------------------------
    # Recreate the collection
    # --------------------------------------------------
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE,
        )
    )

    ingested = 0

    # Make sure test_resumes folder exists
    assert os.path.isdir(TEST_RESUME_DIR), \
        f"Folder not found: {TEST_RESUME_DIR}"

    # --------------------------------------------------
    # Process each PDF in test_resumes/
    # --------------------------------------------------
    for filename in os.listdir(TEST_RESUME_DIR):
        if not filename.lower().endswith(".pdf"):
            continue

        path = os.path.join(TEST_RESUME_DIR, filename)

        # Read file
        with open(path, "rb") as f:
            pdf_bytes = f.read()

        # Convert PDF → text
        text = extract_text_from_pdf_bytes(pdf_bytes)
        assert text.strip(), f"Could not extract text from {filename}"

        # Embed + store
        vs.add_texts(
            texts=[text],
            metadatas=[{"filename": filename}],
            ids=[str(uuid4())]  # <-- FIXED: QdrantLocal requires UUID strings
        )

        ingested += 1

    # Make sure at least one PDF was processed
    assert ingested > 0, "No PDFs found in test_resumes/"

    # --------------------------------------------------
    # Validate stored count matches ingested count
    # --------------------------------------------------
    col_info = client.get_collection(collection_name=COLLECTION_NAME)

    assert col_info.points_count == ingested, \
        f"Expected {ingested} points but found {col_info.points_count}"

    print(f"\n✔ Successfully ingested {ingested} resumes into Qdrant!")

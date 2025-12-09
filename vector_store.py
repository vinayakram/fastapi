# vector_store.py

import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

COLLECTION_NAME = "resume_vectors"
QDRANT_PATH = "qdrant_storage"   # persistent folder


# ------------------------------
# Create ONE persistent local Qdrant instance
# ------------------------------
_qdrant = QdrantClient(
    path=QDRANT_PATH,
    prefer_grpc=False
)


# Prevent shutdown crash errors on Windows
def safe_close(self=None):
    try:
        _qdrant.close()
    except Exception:
        pass

QdrantClient.__del__ = safe_close


def qdrant_client():
    return _qdrant


# ------------------------------
# OpenAI Embeddings (1536 dims)
# ------------------------------
def embedding():
    return OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="text-embedding-3-small"  # 1536 dims
    )


# ------------------------------
# Initialize collection ONCE
# ------------------------------
def init_qdrant():
    client = qdrant_client()
    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if COLLECTION_NAME not in existing:
        print(f"Creating Qdrant collection: {COLLECTION_NAME}")

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )
    else:
        print(f"Qdrant collection already exists: {COLLECTION_NAME}")


# Run on import
init_qdrant()


# ------------------------------
# LangChain Qdrant Wrapper
# ------------------------------
def vector_store():
    return QdrantVectorStore(
        client=qdrant_client(),
        collection_name=COLLECTION_NAME,
        embedding=embedding(),
    )

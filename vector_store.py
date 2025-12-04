import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings

COLLECTION_NAME = "resume_vectors"

# -------------------------------------
# Create ONE global in-memory Qdrant client
# -------------------------------------
_qdrant = QdrantClient(location=":memory:", prefer_grpc=False)


def qdrant_client():
    return _qdrant   # always return SAME instance


def embeddings():
    return OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="text-embedding-3-small"
    )


# Initialize collection ONCE
def init_qdrant():
    client = qdrant_client()
    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            ),
        )


# Initialize at import
init_qdrant()


def vector_store():
    return Qdrant(
        client=qdrant_client(),            # SAME instance
        collection_name=COLLECTION_NAME,
        embeddings=embeddings(),
    )

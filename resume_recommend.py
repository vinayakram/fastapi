from fastapi import APIRouter, HTTPException
from langchain_openai import OpenAIEmbeddings
from vector_store import qdrant_client, COLLECTION_NAME
from pydantic import BaseModel
import os

router = APIRouter()

class RecommendRequest(BaseModel):
    job_description: str
    top_k: int = 5


@router.post("/recommend-resumes")
async def recommend_resumes(data: RecommendRequest):
    client = qdrant_client()
    
    # Create embedding for the job description
    embedder = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="text-embedding-3-small"
    )

    job_vector = embedder.embed_query(data.job_description)

    # Search Qdrant collection
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=job_vector,
        limit=data.top_k
    )

    # Format results
    recommendations = [
        {
            "score": hit.score,
            "metadata": hit.payload
        }
        for hit in results
    ]

    return {"recommendations": recommendations}

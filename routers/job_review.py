from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()

router = APIRouter()

class JobDescriptionInput(BaseModel):
    job_description: str

@router.post("/review-job")
async def review_job(data: JobDescriptionInput):

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-5.1-chat-latest"   # --> required for lab
    )

    # ---------------------------------
    # PROMPT 1: Identify problems
    # ---------------------------------
    prompt1 = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert HR reviewer. Identify every issue in the job description."
        ),
        (
            "human",
            "Job Description:\n\n{job_description}\n\nList all problems clearly."
        ),
    ])
    chain1 = prompt1 | llm
    summary = chain1.invoke({"job_description": data.job_description}).content

    # ---------------------------------
    # PROMPT 2: Rewrite the weak parts
    # ---------------------------------
    prompt2 = ChatPromptTemplate.from_messages([
        (
            "system",
            "Rewrite only the weak or unclear parts of the job description."
        ),
        (
            "human",
            "Here are the problems:\n\n{summary}\n\nRewrite only the problematic parts:"
        ),
    ])
    chain2 = prompt2 | llm
    rewritten = chain2.invoke({"summary": summary}).content

    # ---------------------------------
    # PROMPT 3: Produce final fixed JD
    # ---------------------------------
    prompt3 = ChatPromptTemplate.from_messages([
        (
            "system",
            "Create a fully improved, rewritten job description."
        ),
        (
            "human",
            "Original Description:\n{original}\n\n"
            "Rewritten Sections:\n{rewritten}\n\n"
            "Now return a fully fixed job description:"
        ),
    ])
    chain3 = prompt3 | llm
    fixed = chain3.invoke({
        "original": data.job_description,
        "rewritten": rewritten
    }).content

    # API RESPONSE
    return {
        "summary": summary,
        "rewritten": rewritten,
        "fixed": fixed
    }

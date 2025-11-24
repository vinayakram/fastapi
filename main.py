from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine,text
import shutil
from dbconnect import get_db_session
import os
from config import settings
from models import JobBoard, JobPost

app = FastAPI()

LOGO_FOLDER = "static/logos"
os.makedirs(LOGO_FOLDER, exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------
# JOB BOARDS DATA
# -------------------------
#jobboards = {
#    "acme": [
#        {"title": "Customer Support Executive", "description": "L3 Support"},
#        {"title": "Project Manager", "description": "Manages a team of 2"},
#    ],
#    "pcg": [
#        {"title": "Technical Architect", "description": "Solution Architect"},
#        {"title": "Junior Software Engineer", "description": "Code in C"},
#    ],
#    "atlas": [
#        {"title": "Lead Engineer", "description": "Lead a team of 2"}
#    ]
#}

#@app.get("/api/job-boards/{company}")
#async def get_job_board(company: str):
#    company = company.lower()
#    if company not in jobboards:
#        raise HTTPException(status_code=404, detail="Company not listed")

#   return {
#        "company": company,
#       "logo": f"/static/logos/{company}.png",
#       "jobs": jobboards[company]
#   }

@app.get("/api/job-boards/{slug}")
async def get_job_board(slug: str, request: Request):
    slug = slug.lower()

    with get_db_session() as session:
        board = session.query(JobBoard).filter(JobBoard.slug == slug).first()

        if not board:
            raise HTTPException(status_code=404, detail="Company not listed")

        # Absolute URL fix
        base_url = str(request.base_url).rstrip("/")

        return {
            "id": board.id,
            "slug": board.slug,
            "logo": f"{base_url}/static/logos/{slug}.png",
            "jobs": [
                {
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                    "job_board_id": post.job_board_id
                }
                for post in board.job_posts
            ],
        }

# SIMPLE TEST API
# -------------------------
@app.get("/api/vite_testing")
async def vite_testing():
    return [
        {"title": "Customer Support Executive", "description": "Responsible for assisting customers"}
    ]

# -------------------------
# BASIC ROUTES
# -------------------------
@app.get("/api")
async def root():
    return {"status": "hello world deploy"}

@app.get("/api/health")
async def health():
    # Test the connection
    try:
        with get_db_session() as session:
            session.execute(text("select 1"))
            return {"status": "DB connection working"} 
    except Exception as e:
        return {"status": "DB connection not working", "message": str(e)}
        
@app.get("/api/job-boards")
async def api_job_boards():
    with get_db_session() as session:
        jobBoards = session.query(JobBoard).all()
        return jobBoards
        
@app.get("/api/job-boards/{job_board_id}/job-posts")
async def get_job_posts(job_board_id: int):
    with get_db_session() as session:
        posts = (
            session.query(JobPost)
            .filter(JobPost.job_board_id == job_board_id)
            .all()
        )

        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for this board")

        return [
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "job_board_id": post.job_board_id,
            }
            for post in posts
        ]

     
 
# -------------------------
# SERVE REACT BUILD
# -------------------------
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")

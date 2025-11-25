from fastapi import FastAPI, HTTPException, Request,Form,UploadFile,File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from typing import Annotated
from sqlalchemy import text
from pydantic import BaseModel,Field
from pathlib import Path
from config import settings
from supabase import create_client,Client
import os
from dbconnect import get_db_session
from models import JobBoard, JobPost

app = FastAPI()

supabase: Client=create_client(str(settings.SUPABASE_URL),settings.SUPABASE_KEY)

LOGO_FOLDER = Path("static/logos")
os.makedirs(LOGO_FOLDER, exist_ok=True)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

if not settings.PRODUCTION:
    app.mount("/uploads",StaticFiles(directory="uploads"))

# -----------------------------------------------------
# GET A SINGLE JOB BOARD
# -----------------------------------------------------
@app.get("/api/job-boards/{slug}")
async def get_job_board(slug: str, request: Request):
    slug = slug.lower()

    with get_db_session() as session:
        board = session.query(JobBoard).filter(JobBoard.slug == slug).first()

        if not board:
            raise HTTPException(status_code=404, detail="Company not listed")

        base_url = str(request.base_url).rstrip("/")

        return {
            "id": board.id,
            "slug": board.slug,
            "logo": f"{base_url}/static/logos/uploads/{slug}.png",
            "jobs": [
                {
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                    "job_board_id": post.job_board_id,
                }
                for post in board.job_posts
            ],
        }

def upload_file(filename: str, contents: bytes):

    if settings.PRODUCTION:
        bucket = settings.SUPABASE_BUCKET
        path = filename
        content_type = "image/png"

        response = supabase.storage.from_(bucket).upload(
            path,
            contents,
            {
                "content-type": content_type,
                "upsert": "true"
            }
        )

        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket}/{filename}"

    else:
        file_path = UPLOAD_DIR / filename
        with open(file_path, "wb") as f:
            f.write(contents)
        return f"/uploads/{filename}"

    
# -----------------------------------------------------
# SIMPLE TEST API
# -----------------------------------------------------
@app.get("/api/vite_testing")
async def vite_testing():
    return [{"title": "Customer Support Executive", "description": "Responsible for assisting customers"}]
      

# -----------------------------------------------------
# HEALTH CHECK
# -----------------------------------------------------
@app.get("/api")
async def root():
    return {"status": "hello world deploy"}

@app.get("/api/health")
async def health():
    try:
        with get_db_session() as session:
            session.execute(text("select 1"))
            return {"status": "DB connection working"}
    except Exception as e:
        return {"status": "DB connection not working", "message": str(e)}

# -----------------------------------------------------
# LIST ALL JOB BOARDS (FIXED VERSION)
# -----------------------------------------------------
@app.get("/api/job-boards")
async def api_job_boards():
    with get_db_session() as session:
        jobBoards = session.query(JobBoard).all()

        return [
            {
                "id": jb.id,
                "slug": jb.slug,
                "name": getattr(jb, "name", None),
                "logo_url": jb.logo_url
            }
            for jb in jobBoards
        ]

# -----------------------------------------------------
# GET JOB POSTS BY BOARD ID
# -----------------------------------------------------
@app.get("/api/job-boards/{job_board_id}/job-posts")
async def get_job_posts(job_board_id: int):
    with get_db_session() as session:
        posts = session.query(JobPost).filter(JobPost.job_board_id == job_board_id).all()

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

# -----------------------------------------------------
# SERVE REACT BUILD
# -----------------------------------------------------
app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))


class JobBoardForm(BaseModel):
    slug : str = Field(...,min_length=3,max_length=20)
    logo: UploadFile = File(...)


@app.post("/api/job-boards")
async def api_create_or_update_job_board(
    slug: Annotated[str, Form(min_length=3, max_length=20)],
    logo: Annotated[UploadFile, File(...)],
):
    safe_slug = slug.strip().lower()

    contents = await logo.read()
    filename = f"{safe_slug}.png"

    # Always use upload_file()
    logo_url = upload_file(filename, contents)

    with get_db_session() as session:
        board = session.query(JobBoard).filter(JobBoard.slug == safe_slug).first()

        if board:
            board.logo_url = logo_url
            session.commit()
            session.refresh(board)
            return {
                "id": board.id,
                "slug": safe_slug,
                "logo_url": logo_url,
                "message": "Job board updated!",
                "updated": True
            }

        # Create new
        new_board = JobBoard(slug=safe_slug, logo_url=logo_url)
        session.add(new_board)
        session.commit()
        session.refresh(new_board)

        return {
            "id": new_board.id,
            "slug": safe_slug,
            "logo_url": logo_url,
            "message": "Job board created!",
            "updated": False
        }


@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    indexFilePath = os.path.join("frontend", "build", "client", "index.html")
    return FileResponse(path=indexFilePath, media_type="text/html")


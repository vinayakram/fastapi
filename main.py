from fastapi import FastAPI, HTTPException, Request,Form,UploadFile,File,Response,Depends, Cookie,BackgroundTasks
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
from auth import authenticate_admin, require_admin,AdminSessionMiddleware,AdminAuthzMiddleware,delete_admin_session
from models import *
from emailer import send_email


app = FastAPI()
app.add_middleware(AdminAuthzMiddleware)
app.add_middleware(AdminSessionMiddleware)

supabase: Client=create_client(str(settings.SUPABASE_URL),settings.SUPABASE_KEY)

LOGO_FOLDER = Path("static/logos")
os.makedirs(LOGO_FOLDER, exist_ok=True)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

if not settings.PRODUCTION:
    app.mount("/uploads",StaticFiles(directory="uploads"))

class JobDescriptionCheckRequest(BaseModel):
    title: str
    description: str

class AdminLoginForm(BaseModel):
   username : str
   password : str

@app.post("/api/admin-login")
async def admin_login(
    response: Response,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    auth_response = authenticate_admin(username, password)

    if auth_response:
        secure = settings.PRODUCTION
        response.set_cookie(
            key="admin_session",
            value=auth_response,
            httponly=True,
            secure=secure,
            samesite="Lax"
        )
        return {"message": "Login successful"}

    raise HTTPException(status_code=400, detail="Invalid admin credentials")


@app.post("/api/check-job-description")
async def check_job_description(title: str = Form(...), description: str = Form(...)):
    """
    Uses AI to validate if the job description matches the job title.
    Returns a score and explanation.
    """
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")  # Or gpt-3.5-turbo

    prompt = ChatPromptTemplate.from_template(
        "You are a HR assistant AI. "
        "Evaluate if the following job description suits the job title.\n\n"
        "Job Title: {title}\n"
        "Job Description: {description}\n\n"
        "Answer in JSON format with:\n"
        " - is_suitable: true/false\n"
        " - reason: short explanation."
    )

    message = prompt.format_messages(title=title, description=description)

    response = llm(message)
    # LangChain returns AI output as string
    import json
    try:
        result = json.loads(response.content)  # expects JSON like {"is_suitable": true, "reason": "..."}
    except:
        # fallback if AI doesn't output valid JSON
        result = {"is_suitable": None, "reason": response.content}

    return result
    
@app.get("/api/me")
async def me(req: Request):
        return {"is_admin": req.state.is_admin}
 
@app.post("/api/admin-logout")
async def admin_logout(request: Request, response: Response):
        delete_admin_session(request.cookies.get("admin_session"))
        secure=settings.PRODUCTION
        response.delete_cookie(key="admin_session",httponly=True,secure=secure,samesite="Lax")
        return{}
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
                for post in board.job_posts if post.status == "open"
            ],
        }
def evaluate_resume(resume_content, job_post_description, job_application_id):
   resume_raw_text = extract_text_from_pdf_bytes(resume_content)
   ai_evaluation = evaluate_resume_with_ai(resume_raw_text, job_post_description)
   with get_db_session() as session:
      evaluation = JobApplicationAIEvaluation(
         job_application_id = job_application_id,
         overall_score = ai_evaluation["overall_score"],
         evaluation = ai_evaluation
      )
      session.add(evaluation)
      session.commit()
      
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
        return f"http://localhost:8000/uploads/{filename}"


def upload_resume(filename: str, contents: bytes):

    if settings.PRODUCTION:
        bucket = settings.SUPABASE_BUCKET_RESUME
        path = f"resumes/{filename}"
        content_type = "application/pdf"

        response = supabase.storage.from_(bucket).upload(
            path,
            contents,
            {"content-type": content_type, "x-upsert": "true"}
        )

        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket}/{path}"

    else:
        file_path = UPLOAD_DIR / "resumes"
        file_path.mkdir(exist_ok=True)
        full_path = file_path / filename

        with open(full_path, "wb") as f:
            f.write(contents)

        return f"/uploads/resumes/{filename}"

  
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
        posts = session.query(JobPost).filter(JobPost.job_board_id == job_board_id,JobPost.status == "open").all()

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
    is_admin: bool = Depends(require_admin)
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

@app.get("/api/job-boards/id/{board_id}")
async def get_board_by_id(board_id: int):
    with get_db_session() as session:
        board = session.query(JobBoard).filter(JobBoard.id == board_id).first()

        if not board:
            raise HTTPException(status_code=404, detail="Job board not found")

        return {
            "id": board.id,
            "slug": board.slug,
            "logo_url": board.logo_url,
            "jobs": [
                {
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                    "job_board_id": post.job_board_id,
                }
                for post in board.job_posts if post.status == "open"
            ]
        }


@app.post("/api/job-posts")
async def create_job_post(
    job_board_id: Annotated[int, Form()],
    title: Annotated[str, Form()],
    description: Annotated[str, Form()]
):
    with get_db_session() as session:
        # Ensure job board exists
        board = session.query(JobBoard).filter(JobBoard.id == job_board_id).first()
        if not board:
            raise HTTPException(404, "Invalid job_board_id")

        new_post = JobPost(
            job_board_id=job_board_id,
            title=title,
            description=description,
            status="open"
        )

        session.add(new_post)
        session.commit()
        session.refresh(new_post)

        return {
            "message": "Job post created successfully",
            "post": {
                "id": new_post.id,
                "job_board_id": new_post.job_board_id,
                "title": new_post.title,
                "description": new_post.description,
                "status": new_post.status
            }
        }


@app.put("/api/job-posts/{post_id}/status")
async def update_job_status(
    post_id: int,
    status: Annotated[str, Form(min_length=4, max_length=10)]
):
    status = status.lower()

    if status not in ["open", "closed"]:
        raise HTTPException(400, "Status must be 'open' or 'closed'")

    with get_db_session() as session:
        job_post = session.query(JobPost).filter(JobPost.id == post_id).first()

        if not job_post:
            raise HTTPException(404, "Job post not found")

        job_post.status = status
        session.commit()

        return {
            "message": f"Job post {post_id} marked as {status}",
            "id": post_id,
            "status": status
        }

@app.get("/api/job-posts")
async def list_all_job_posts(status: str = "open"):
    status = status.lower()
    if status not in ["open", "closed", "all"]:
        raise HTTPException(400, "Invalid status filter")

    with get_db_session() as session:
        query = session.query(JobPost)

        if status != "all":
            query = query.filter(JobPost.status == status)

        posts = query.all()

        return [
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "status": post.status,
                "job_board_id": post.job_board_id,
            }
            for post in posts
        ]


@app.post("/api/job-applications")
@app.post("/api/job-applications")
async def create_job_application(
    background_tasks: BackgroundTasks,
    job_post_id: Annotated[int, Form()],
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    resume: Annotated[UploadFile, File(...)]
):
    contents = await resume.read()
    filename = f"{first_name}_{last_name}_{resume.filename}"

    resume_url = upload_resume(filename, contents)

    with get_db_session() as session:
        post = session.query(JobPost).filter(JobPost.id == job_post_id).first()
        if not post:
            raise HTTPException(404, "Invalid job_post_id")

        if post.status == "closed":
            raise HTTPException(400, "This job post is closed and cannot accept applications")

        application = JobApplication(
            job_post_id=job_post_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            resume_url=resume_url
        )

        session.add(application)
        session.commit()
        session.refresh(application)

        # IMPORTANT: Extract data BEFORE session closes
        post_title = post.title
        application_id = application.id

    # Build email message OUTSIDE the session
    subject = "Job Application Received"

    body = f"""
        <h3>Hi {first_name},</h3>
        <p>Your application for <strong>{post_title}</strong> has been submitted.</p>
        <p>We will contact you soon.</p>
    """

    # Background email task
    background_tasks.add_task(send_email, email, subject, body)
    background_tasks.add_task(evaluate_resume, resume_content, jobPost.description, new_job_application.id)

    return {
        "message": "Application submitted successfully",
        "application_id": application_id,
        "resume_url": resume_url
    }

@app.get("/api/job-applications")
async def list_job_applications():
    with get_db_session() as session:
        apps = session.query(JobApplication).all()

        return [
            {
                "id": a.id,
                "job_post_id": a.job_post_id,
                "first_name": a.first_name,
                "last_name": a.last_name,
                "email": a.email,
                "resume_url": a.resume_url
            }
            for a in apps
        ]


@app.delete("/api/job-boards/id/{board_id}")
async def delete_job_board(board_id: int):
    with get_db_session() as session:
        board = session.query(JobBoard).filter(JobBoard.id == board_id).first()

        if not board:
            raise HTTPException(404, "Job board not found")

        session.delete(board)
        session.commit()

        return {"message": f"Job board {board_id} deleted"}

@app.put("/api/job-boards/{board_id}")
async def api_update_job_board(
    board_id: int,
    slug: Annotated[str, Form(min_length=3, max_length=20)],
    logo: UploadFile | None = File(None)
):
    safe_slug = slug.strip().lower()

    with get_db_session() as session:
        board = session.query(JobBoard).filter(JobBoard.id == board_id).first()

        if not board:
            raise HTTPException(404, "Job board not found")

        # update slug
        board.slug = safe_slug

        # update logo only if provided
        if logo:
            contents = await logo.read()
            filename = f"{safe_slug}.png"
            logo_url = upload_file(filename, contents)
            board.logo_url = logo_url

        session.commit()
        session.refresh(board)

        return {
            "message": "Job board updated",
            "id": board.id,
            "slug": board.slug,
            "logo_url": board.logo_url,
        }



@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    indexFilePath = os.path.join("frontend", "build", "client", "index.html")
    return FileResponse(path=indexFilePath, media_type="text/html")


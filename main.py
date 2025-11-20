from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import shutil
import os

app = FastAPI()

LOGO_FOLDER = "static/logos"
os.makedirs(LOGO_FOLDER, exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------
# JOB BOARDS DATA
# -------------------------
jobboards = {
    "acme": [
        {"title": "Customer Support Executive", "description": "L3 Support"},
        {"title": "Project Manager", "description": "Manages a team of 2"},
    ],
    "pcg": [
        {"title": "Technical Architect", "description": "Solution Architect"},
        {"title": "Junior Software Engineer", "description": "Code in C"},
    ],
    "atlas": [
        {"title": "Lead Engineer", "description": "Lead a team of 2"}
    ]
}

@app.get("/api/job-boards/{company}")
async def get_job_board(company: str):
    company = company.lower()
    if company not in jobboards:
        raise HTTPException(status_code=404, detail="Company not listed")

    return {
        "company": company,
        "logo": f"/static/logos/{company}.png",
        "jobs": jobboards[company]
    }

# -------------------------
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



# -------------------------
# SERVE REACT BUILD
# -------------------------
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")

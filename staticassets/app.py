from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    html_content = """
    <html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <h1>Hello from FastAPI</h1>
            <img src="/static/images/logo.png" width="150">
            <script src="/static/script.js"></script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/static-job-board.html")
async def static_job_board():
	return HTMLResponse("<h3>Hello</h3>")

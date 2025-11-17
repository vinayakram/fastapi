from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "hello world deploy"}

@app.get("/health")
async def health():
  return {"status": "ok"}


@app.get("/add")
async def add(x : int, y : int):
    return { "result" : xvalue+yvalue }

@app.get("/multiply")
async def multiply(x : int, y: int):
    return { "result" : x*y }

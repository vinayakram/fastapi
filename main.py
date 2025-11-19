from fastapi import FastAPI,HTTPException

app = FastAPI()

jobboards = { "acme" : [{"title": "customer support executive","job description":"L3"},{"title":"project manager","job description":"manage a team of 2"}],
              "pcg" : [{"title": "technical architect","job description":"solution architect"},{"title":"junior software engineer","job description":"code in c"}],
              "atlas" : [{"title": "lead engineer","job description":"lead a team of 2"}]
              }
              

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
    
    
@app.get("/job-boards/{q}")
async def jobboard(q: str):
        if q not in jobboards:
            raise HTTPException(
                status_code=404,
                detail="Company not listed",
                headers={"Company not listed": "Error"}
                )
        return jobboards[q]
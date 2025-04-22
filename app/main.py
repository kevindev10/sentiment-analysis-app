from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from database import get_db, engine
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
import crud, database, models, schemas, utils



# Create the database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Setup for Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
  return templates.TemplateResponse("index2.html", {"request": request})


@app.post("/generate/")
async def generate_content(payload: schemas.GeneratePayload, db: Session = Depends(get_db)):
  generated_text = await run_in_threadpool(utils.generate_content, db, payload.topic)
  return {"generated_text": generated_text}



@app.post("/analyze/")
async def analyze_content(payload: schemas.AnalyzePayload, db: Session = Depends(get_db)):
    readability, sentiment = await run_in_threadpool(utils.analyze_content, db, payload.content)
    return {"readability": readability, "sentiment": sentiment}

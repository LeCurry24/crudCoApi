import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models.url import Urls
from sqlmodel import Session, select


from config import settings
from db import get_session

app = FastAPI()

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Root Route"}

@app.get("/urls")
def list_url(session: Session = Depends(get_session)):
    statement = select(Urls).order_by(Urls.creation_date)
    result = session.exec(statement).first()
    return result

@app.post("/urls/add")
def add_url(url: Urls, session: Session = Depends(get_session)):
    new_url = Urls(**url.model_dump())
    print(new_url)
    session.add(new_url)
    session.commit()
    session.refresh(new_url)
    return {"URL ADDED:", new_url.name}

@app.get("/users")
def list_url(session: Session = Depends(get_session)):
    statement = select(Users)
    result = session.exec(statement).first()
    return result

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from models.url import Urls
from models.users import User
from sqlmodel import Session, select
from nanoid import generate
from datetime import timedelta

from config import settings
from db import get_session
from config import settings
from models.tokens import Token, create_access_token, timedelta

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

def lookup_user(username: str, session: Session = Depends(get_session)):
    return session.query(user).filter(user.username == form_data.username).one()

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
    new_url.short_url = generate(size=8)
    session.add(new_url)
    session.commit()
    session.refresh(new_url)
    return {"URL ADDED:", new_url.title}


@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  session: Session = Depends(get_session) ):
    try:
        user = lookup_user(form_data.username, session)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    is_validated: bool = user.validate_password(form_data.password)

    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post('/users/add')
async def add_user(user_data: User, session: Session = Depends(get_session)):
    new_user = User(**user_data.model_dump())
    new_user.hashed_password = User.hash_password(new_user.hashed_password);
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"User added:", new_user.username}

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
import univorn
from fastapi import FastAPI, Depends
from fastapi.middleware.corn import CORSMiddleware

from sqlmodel import session, select


# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173"
]

app = FastAPI()

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Root Route"}
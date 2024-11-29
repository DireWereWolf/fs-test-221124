from typing import Union

from fastapi import FastAPI
from app.routers import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
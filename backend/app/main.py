from fastapi import FastAPI # type: ignore
from app.api import upload

app = FastAPI()

app.include_router(upload.router, prefix="/api")

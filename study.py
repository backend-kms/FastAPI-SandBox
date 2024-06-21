from fastapi import FastAPI

from app.routers import user

app = FastAPI(
    title="FastAPI 스터디 명세서",
    description="",
    version="0.0.1",
)

app.include_router(user.router, prefix="/api")

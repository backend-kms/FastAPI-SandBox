from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import admin, user

app = FastAPI(
    title="FastAPI 스터디 명세서",
    description="",
    version="0.0.1",
)
add_pagination(app)

app.include_router(user.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

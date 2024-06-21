# 1. routers: API 엔드포인트를 정의, 각 엔드포인트는 클라이언트와의 상호작용을 처리

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import model
from app.service.user import UserService
from app.utils import get_db

router = APIRouter(prefix="/user")


@router.post(
    path="/sign-up",
    tags=["user"],
    summary="회원가입",
    status_code=201,
    # responses={},
)
def sign_up(user: model.user.UserCreate, db: Session = Depends(get_db)):
    UserService.sign_up(user, db)
    return True

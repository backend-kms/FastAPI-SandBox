# 2. service: 비지니스 로직을 처리, 유효성 검사, 직렬화 및 비직렬화, db 연결을 제외한 모든 처리 / 데이터베이스와의 직접적인 상호작용은 없음

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import model
from app.repository.user import UserRepository
from app.utils import pwd_context


class UserService:
    @staticmethod
    def sign_up(user: model.user.UserCreate, db: Session):
        is_existed = UserRepository.check_existing_email(user, db)
        if is_existed:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 존재하는 사용자입니다.",
            )
        user.password = pwd_context.hash(user.password)
        db_user = UserRepository.create_user(user, db)
        return db_user

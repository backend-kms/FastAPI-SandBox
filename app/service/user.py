# 2. service: 비지니스 로직을 처리, 유효성 검사, 직렬화 및 비직렬화, db 연결을 제외한 모든 처리 / 데이터베이스와의 직접적인 상호작용은 없음

from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from app import model
from app.enums import UserGender, UserRole
from app.repository.user import UserRepository
from app.utils import pwd_context
from config import ACCESS_TOKEN_EXPIRE_MINUTES, HASH_ALGORITHM, SECRET_KEY


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

    @staticmethod
    def sign_in(user: OAuth2PasswordRequestForm, db: Session):
        db_user = UserRepository.get_user_by_email(user.username, db)
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="아이디와 비밀번호를 확인하세요.",
            )
        seed = {
            "sub": db_user.email,
            "exp": datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
        }
        access_token = jwt.encode(seed, SECRET_KEY, algorithm=HASH_ALGORITHM)
        UserRepository.update_last_login(db_user, access_token, db)

        response = dict(access_token=access_token, username=db_user.username)

        return response

    @staticmethod
    def sign_out(token: str, db: Session):
        # db_user = UserRepository.get_user_by_token(token, db) # 로그를 저장안하기 떄문에 아직 필요 x
        UserRepository.remove_access_token(token, db)

    @staticmethod
    def get_user_profile(token: str, db: Session):
        db_user = UserRepository.get_user_by_token(token, db)
        return dict(
            email=db_user.email,
            username=db_user.username,
            gender=UserGender[db_user.gender.upper()].display,
            age=f"{db_user.age}세",
            role=UserRole[db_user.role.upper()].display,
        )
